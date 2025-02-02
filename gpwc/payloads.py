from typing import Literal, Optional
from abc import ABC

from .utils import generate_id


class Payload(ABC):
    rpcid: str
    data: list[str | None]
    payload_id: str
    parse_response: bool

    def __init__(self):
        self.payload_id: str = generate_id()


class GetItemsByTakenDate(Payload):
    def __init__(
        self,
        timestamp: Optional[int] = None,
        source: Optional[Literal["library", "archive", "both"]] = "both",
        page_id: Optional[str] = None,
        page_size: Optional[int] = 500,
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        source_map = {"library": 1, "archive": 2, "both": 3}
        self.parse_response = parse_response
        self.rpcid = "lcxiM"
        self.data = [page_id, timestamp, page_size, None, 1, source_map[source]]


class GetItemsByUploadedDate(Payload):
    def __init__(
        self,
        page_id: Optional[str] = None,
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        self.parse_response = parse_response
        self.rpcid = "EzkLib"
        self.data = ["", [[4, "ra", 0, 0]], page_id]


class Search(Payload):
    def __init__(
        self,
        query: str,
        page_id: Optional[str] = None,
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        self.parse_response = parse_response
        self.rpcid = "EzkLib"
        self.data = [query, None, page_id]


class GetRemoteMatchesByHash(Payload):
    def __init__(
        self,
        hashes: list[str],
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        self.parse_response = parse_response
        self.rpcid = "swbisb"
        self.data = [hashes, None, 3, 0]
