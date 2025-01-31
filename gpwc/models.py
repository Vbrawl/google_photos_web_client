from dataclasses import dataclass


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
