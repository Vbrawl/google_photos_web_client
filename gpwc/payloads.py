from typing import Literal, Optional
import uuid

from .models import rpcidPayload


def get_items_by_taken_date(
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
    return rpcidPayload(rpcid, data, payload_id, parse_response)
