from dataclasses import dataclass


@dataclass
class ApiResponse:
    rpcid: str
    data: list | dict
    success: bool
    response_id: str
