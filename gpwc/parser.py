from dataclasses import dataclass
from typing import Optional
from .utils import safe_get


@dataclass
class GeoLocation:
    coordinates: Optional[list[float]] = None
    name: Optional[str] = None


@dataclass
class LibraryItem:
    media_key: str = None
    timestamp: int = None
    timezone_offset: int = None
    creation_timestamp: int = None
    dedup_key: str = None
    thumbnail_url: str = None
    res_width: int = None
    res_height: int = None
    is_partial_upload: bool = False
    is_archived: bool = None
    is_favorite: bool = None
    video_duration: Optional[int] = None
    description_short: Optional[str] = None
    is_live_photo: bool = False
    live_photo_duration: Optional[int] = None
    is_owned: bool = False
    geo_location: GeoLocation = None

    @classmethod
    def from_data(cls, item_data):
        # Parse geo_location if present
        geo_location = None
        if safe_get(item_data, -1, "129168200", 1) is not None:
            geo_location = GeoLocation(
                coordinates=safe_get(item_data, -1, "129168200", 1, 0),
                name=safe_get(item_data, -1, "129168200", 1, 4, 0, 1, 0, 0),
            )

        return cls(
            media_key=safe_get(item_data, 0),
            timestamp=safe_get(item_data, 2),
            timezone_offset=safe_get(item_data, 4),
            creation_timestamp=safe_get(item_data, 5),
            dedup_key=safe_get(item_data, 3),
            thumbnail_url=safe_get(item_data, 1, 0),
            res_width=safe_get(item_data, 1, 1),
            res_height=safe_get(item_data, 1, 2),
            is_partial_upload=safe_get(item_data, 12, 0) == 20,
            is_archived=safe_get(item_data, 13),
            is_favorite=safe_get(item_data, -1, "163238866", 0),
            video_duration=safe_get(item_data, -1, "76647426", 0),
            description_short=safe_get(item_data, -1, "396644657", 0),
            is_live_photo=safe_get(item_data, -1, "146008172") is not None,
            live_photo_duration=safe_get(item_data, -1, "146008172", 1),
            is_owned=not any(27 in sub_array for sub_array in safe_get(item_data, 7, default=[])),
            geo_location=geo_location,
        )


@dataclass
class LibraryTimelinePage:
    items: list[LibraryItem]
    next_page_id: Optional[str]
    last_item_timestamp: Optional[int]

    @classmethod
    def from_data(cls, data):
        return cls(
            items=[LibraryItem.from_data(item) for item in safe_get(data, 0, default=[])],
            next_page_id=safe_get(data, 1),
            last_item_timestamp=safe_get(data, 2) and int(safe_get(data, 2)),
        )


@dataclass
class LibraryGenericPage:
    items: list[LibraryItem]
    next_page_id: Optional[str]

    @classmethod
    def from_data(cls, data):
        return cls(
            items=[LibraryItem.from_data(item) for item in safe_get(data, [0]) or []],
            next_page_id=safe_get(data, [1]),
        )


@dataclass
class RemoteMatch:
    hash: str = None
    media_key: str = None
    thumb: str = None
    res_width: int = None
    res_height: int = None
    timestamp: int = None
    dedup_key: str = None
    timezone_offset: int = None
    creation_timestamp: int = None
    video_duration: Optional[int] = None
    camera_info: Optional[str] = None

    @classmethod
    def from_data(cls, item_data):
        return cls(
            hash=safe_get(item_data, 0),
            media_key=safe_get(item_data, 1, 0),
            thumb=safe_get(item_data, 1, 1, 0),
            res_width=safe_get(item_data, 1, 1, 1),
            res_height=safe_get(item_data, 1, 1, 2),
            timestamp=safe_get(item_data, 1, 2),
            dedup_key=safe_get(item_data, 1, 3),
            timezone_offset=safe_get(item_data, 1, 4),
            creation_timestamp=safe_get(item_data, 1, 5),
            video_duration=safe_get(item_data, 1, -1, "76647426", 0),
            camera_info=safe_get(item_data, 1, 1, 8),
        )


def parse_response_data(rpc_id: str, data: dict):
    match rpc_id:
        case "lcxiM":
            return LibraryTimelinePage.from_data(data)
        case "EzkLib":
            return LibraryGenericPage.from_data(data)
        case "swbisb":
            return [RemoteMatch.from_data(item) for item in safe_get(data, [0]) or []]
        case _:
            return {}
