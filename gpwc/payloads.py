from typing import Literal, Optional
from abc import ABC

from .utils import generate_id


class Payload(ABC):
    rpcid: str
    data: list[str | None]
    payload_id: str
    parse_response: Optional[bool] = False

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


class GetItemInfo(Payload):
    def __init__(
        self,
        media_key: str,
        album_media_key: Optional[str] = None,
        auth_key: Optional[str] = None,
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        self.parse_response = parse_response
        self.rpcid = "VrseUb"
        self.data = [media_key, None, auth_key, None, album_media_key]


class GetItemInfoExt(Payload):
    def __init__(
        self,
        media_key: str,
        auth_key: Optional[str] = None,
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        self.parse_response = parse_response
        self.rpcid = "fDcn4b"
        self.data = [media_key, 1, auth_key, None, 1]


class GetBatchMediaInfo(Payload):
    def __init__(
        self,
        media_keys: list[str],
        parse_response: Optional[bool] = True,
    ):
        super().__init__()
        self.parse_response = parse_response
        keys = [[key] for key in media_keys]
        self.rpcid = "EWgK9e"
        self.data = [[[keys], [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, [], None, None, None, None, None, None, None, None, None, None, []]]]]


class MoveToTrash(Payload):
    def __init__(
        self,
        dedup_keys: list[str],
    ):
        super().__init__()
        self.rpcid = "XwAOJf"
        self.data = [None, 1, dedup_keys, 3]


class RestoreFromTrash(Payload):
    def __init__(
        self,
        dedup_keys: list[str],
    ):
        super().__init__()
        self.rpcid = "XwAOJf"
        self.data = [None, 3, dedup_keys, 2]


class CreateAlbum(Payload):
    def __init__(
        self,
        name: str,
    ):
        super().__init__()
        self.rpcid = "OXvT9d"
        self.data = [name, None, 2]


class SetFavorite(Payload):
    def __init__(
        self,
        dedup_keys: list[str],
    ):
        super().__init__()
        self.rpcid = "Ftfh0"
        dedup_keys_list = [[None, key] for key in dedup_keys]
        self.data = [dedup_keys_list, [1]]


class UnFavorite(Payload):
    def __init__(
        self,
        dedup_keys: list[str],
    ):
        super().__init__()
        self.rpcid = "Ftfh0"
        dedup_keys_list = [[None, key] for key in dedup_keys]
        self.data = [dedup_keys_list, [2]]


class SetArchive(Payload):
    def __init__(
        self,
        dedup_keys: list[str],
    ):
        super().__init__()
        self.rpcid = "w7TP3c"
        dedup_keys_list = [[None, [1], [None, key]] for key in dedup_keys]
        self.data = [dedup_keys_list, None, 1]


class UnArchive(Payload):
    def __init__(
        self,
        dedup_keys: list[str],
    ):
        super().__init__()
        self.rpcid = "w7TP3c"
        dedup_keys_list = [[None, [2], [None, key]] for key in dedup_keys]
        self.data = [dedup_keys_list, None, 1]
