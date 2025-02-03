from dataclasses import dataclass
from typing import Optional
from .utils import safe_get


@dataclass
class GeoLocation:
    coordinates: Optional[list[float]]
    name: Optional[str]


@dataclass
class LibraryItem:
    media_key: str
    timestamp: int
    timezone_offset: int
    creation_timestamp: int
    dedup_key: str
    thumbnail_url: str
    res_width: int
    res_height: int
    is_partial_upload: bool
    is_archived: bool
    is_favorite: bool
    video_duration: Optional[int]
    description_short: Optional[str]
    is_live_photo: bool
    live_photo_duration: Optional[int]
    is_owned: bool
    geo_location: GeoLocation

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
    hash: str
    media_key: str
    thumb: str
    res_width: int
    res_height: int
    timestamp: int
    dedup_key: str
    timezone_offset: int
    creation_timestamp: int
    video_duration: Optional[int]
    camera_info: Optional[str]

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


@dataclass
class ItemInfo:
    media_key: str
    dedup_key: str
    res_width: int
    res_height: int
    is_partial_upload: bool
    timestamp: int
    timezone_offset: int
    creation_timestamp: int
    download_url: str
    download_original_url: str
    saved_to_your_photos: bool
    is_archived: bool
    space_taken: int
    is_original_quality: bool
    is_favorite: bool
    thumbnail_url: str
    is_live_photo: bool
    video_duration: Optional[int]
    live_photo_duration: Optional[int]
    live_photo_video_download_url: Optional[str]
    trash_timestamp: Optional[int]
    description_full: Optional[str]

    @classmethod
    def from_data(cls, item_data):
        """
        Constructs an ItemInfo instance from the given nested item_data structure.
        Uses safe_get to safely access nested values.
        """
        return cls(
            media_key=safe_get(item_data, 0, 0),
            dedup_key=safe_get(item_data, 0, 3),
            res_width=safe_get(item_data, 0, 1, 1),
            res_height=safe_get(item_data, 0, 1, 2),
            is_partial_upload=safe_get(item_data, 0, 12, 0) == 20,
            timestamp=safe_get(item_data, 0, 2),
            timezone_offset=safe_get(item_data, 0, 4),
            creation_timestamp=safe_get(item_data, 0, 5),
            download_url=safe_get(item_data, 1),
            download_original_url=safe_get(item_data, 7),
            saved_to_your_photos=len(safe_get(item_data, 0, 15, "163238866", default=[])) > 0,
            is_archived=safe_get(item_data, 0, 13),
            space_taken=safe_get(item_data, 0, 15, "318563170", 0, 1),
            is_original_quality=(None if safe_get(item_data, 0, 15, "318563170", 0, 2) is None else safe_get(item_data, 0, 15, "318563170", 0, 2) == 2),
            is_favorite=safe_get(item_data, 0, 15, "163238866", 0),
            video_duration=safe_get(item_data, 0, 15, "76647426", 0),
            is_live_photo=safe_get(item_data, 0, 15, "146008172") is not None,
            live_photo_duration=safe_get(item_data, 0, 15, "146008172", 1),
            live_photo_video_download_url=safe_get(item_data, 0, 15, "146008172", 3),
            trash_timestamp=safe_get(item_data, 0, 15, "225032867", 0),
            description_full=safe_get(item_data, 10),
            thumbnail_url=safe_get(item_data, 12),
        )


def parse_response_data(rpc_id: str, data: dict):
    match rpc_id:
        case "lcxiM":
            return LibraryTimelinePage.from_data(data)
        case "EzkLib":
            return LibraryGenericPage.from_data(data)
        case "swbisb":
            return [RemoteMatch.from_data(item) for item in safe_get(data, [0]) or []]
        case "VrseUb":
            return ItemInfo.from_data(data)
        case _:
            return {}
