import http.cookiejar
import json
from dataclasses import dataclass
from typing import Literal, Optional
from pathlib import Path
from http.cookiejar import MozillaCookieJar
import urllib.parse
import uuid

import requests
from lxml import html

from . import utils
from .parser import parse


@dataclass
class rpcidPayload:
    rpcid: str
    data: list[str | None]
    payload_id: str
    parse_response: bool


@dataclass
class ApiResponse:
    rpcid: str
    data: list | dict
    response_id: str


class Client:
    """Reverse engineered Google Photos web API client."""

    def __init__(self, cookies_txt_path: str | Path, log_level: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"] = "INFO") -> None:
        """ """
        self.cookies_txt_path = cookies_txt_path
        self.logger = utils.create_logger(log_level)
        self.session = utils.new_session_with_retries()
        self.load_cookies_in_session()
        self.global_data = self.get_global_data()
        self.logger.info(f"Account: {self.global_data['oPEP7c']}")

    def load_cookies_in_session(self) -> None:
        """Load cookies from cookies.txt and upate session cookies with them"""
        cookies = self.load_cookies_from_file(self.cookies_txt_path)
        self.session.cookies.update(cookies)

    def get_global_data(self) -> dict:
        """Get and parse global_data from photos.google.com page"""
        page_body = self.session.get("https://photos.google.com/").text
        return self.parse_main_page(page_body)

    def parse_main_page(self, page_body: str) -> dict:
        """Parse data from photos.google.com html body"""
        xml_page = html.fromstring(page_body)
        script_node = xml_page.xpath('//script[@data-id="_gd"]')[0]
        script_text: str = script_node.text
        script_json = script_text.replace("window.WIZ_global_data = ", "").replace(";", "")
        return json.loads(script_json)

    def load_cookies_from_file(self, path: str) -> MozillaCookieJar:
        """Load netscape cookies from file"""
        cookie_jar = http.cookiejar.MozillaCookieJar(path)
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        return cookie_jar

    def save_cookies_to_file(self) -> None:
        """Save sesion cookies to file in netscape format"""
        cookie_jar = http.cookiejar.MozillaCookieJar(self.cookies_txt_path)
        requests.utils.cookiejar_from_dict({c.name: c.value for c in self.session.cookies}, cookie_jar)
        cookie_jar.save(ignore_discard=True, ignore_expires=True)

    def get_items_by_taken_date(
        self,
        timestamp: Optional[int] = None,
        source: Optional[Literal["library", "archive", "both"]] = "both",
        page_id: Optional[str] = None,
        page_size: Optional[int] = 500,
        parse_response: Optional[bool] = True,
    ) -> rpcidPayload:
        source_map = {"library": 1, "archive": 2, "both": 3}
        source_id = source_map[source]
        rpcid = "lcxiM"
        data = [page_id, timestamp, page_size, None, 1, source_id]
        payload_id = str(uuid.uuid4()).replace("-", "")
        data = self.prepare_data(rpcid, data, payload_id)
        return rpcidPayload(rpcid, data, payload_id, parse_response)

    def prepare_data(self, rpcid: str, data: list[str | int], payload_id: str) -> list:
        return [rpcid, json.dumps(data, separators=(",", ":")), None, payload_id]

    def send_api_request(self, payloads: list[rpcidPayload]):
        """Send a list of rpcid requests"""
        querystring = {
            "rpcids": ",".join([payload.rpcid for payload in payloads]),
            "source-path": "/",
            "f.sid": self.global_data["FdrFJe"],
            "bl": self.global_data["cfb2h"],
            "rt": "c",
        }
        payload = {"f.req": json.dumps([[payload.data for payload in payloads]], separators=(",", ":")), "at": self.global_data["SNlM0e"]}
        payload_encoded = "&".join(f"{key}={urllib.parse.quote(value, safe='')}" for key, value in payload.items())

        url = f"https://photos.google.com{self.global_data['Im6cmf']}/data/batchexecute"

        response = self.session.post(url, data=payload_encoded, params=querystring)

        response.raise_for_status()

        return self.parse_api_response(response.text, payloads)

    def parse_api_response(self, response_body: str, payloads: list[rpcidPayload]):
        """Parse api response"""
        responses = [json.loads(line) for line in response_body.split("\n") if "wrb.fr" in line]
        parsed_responses = []
        for response in responses:
            response_data = json.loads(response[0][2])
            response_id = response[0][6]
            response_rpcid = response[0][1]
            parse_response = next(payload.parse_response for payload in payloads if payload.payload_id == response_id)
            api_response = ApiResponse(
                rpcid=response_rpcid,
                response_id=response_id,
                data=parse(response_rpcid, response_data) if parse_response else response_data,
            )
            parsed_responses.append(api_response)
        return parsed_responses
