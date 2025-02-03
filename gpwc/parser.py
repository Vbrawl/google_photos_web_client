from dataclasses import dataclass
from typing import Optional
from .utils import safe_get


@dataclass
class GeoLocation:
    coordinates: Optional[list[float]] = None
    name: Optional[str] = None
    map_thumb: Optional[str] = None

    @classmethod
    def from_data(cls, item_data):
        return cls(
            coordinates=safe_get(item_data, 0, 9, 0) or safe_get(item_data, 0, 13, 0),
            name=safe_get(item_data, 0, 13, 2, 0, 1, 0, 0),
            map_thumb=safe_get(item_data, 1),
        )


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
            is_original_quality=safe_get(item_data, 0, 15, "318563170", 0, 2) == 2,
            is_favorite=safe_get(item_data, 0, 15, "163238866", 0),
            video_duration=safe_get(item_data, 0, 15, "76647426", 0),
            is_live_photo=safe_get(item_data, 0, 15, "146008172") is not None,
            live_photo_duration=safe_get(item_data, 0, 15, "146008172", 1),
            live_photo_video_download_url=safe_get(item_data, 0, 15, "146008172", 3),
            trash_timestamp=safe_get(item_data, 0, 15, "225032867", 0),
            description_full=safe_get(item_data, 10),
            thumbnail_url=safe_get(item_data, 12),
        )


@dataclass
class Actor:
    actor_id: Optional[str]
    gaia_id: Optional[str]
    name: Optional[str]
    gender: Optional[str]
    profile_photo_url: Optional[str]

    @classmethod
    def from_data(cls, data):
        return cls(
            actor_id=safe_get(data, 0),
            gaia_id=safe_get(data, 1),
            name=safe_get(data, 11, 0),
            gender=safe_get(data, 11, 2),
            profile_photo_url=safe_get(data, 12, 0),
        )


@dataclass
class Album:
    media_key: str
    owner_actor_id: Optional[str]
    title: Optional[str]
    thumbnail_url: Optional[str]
    item_count: int
    is_shared: bool
    creation_timestamp: int
    modified_timestamp: int
    timestamp_range: Optional[list[Optional[int]]]

    @classmethod
    def from_data(cls, item_data):
        return cls(
            media_key=safe_get(item_data, 0),
            owner_actor_id=safe_get(item_data, 6, 0),
            title=safe_get(item_data, -1, "72930366", 1),
            thumbnail_url=safe_get(item_data, 1, 0),
            item_count=safe_get(item_data, -1, "72930366", 3),
            creation_timestamp=safe_get(item_data, -1, "72930366", 2, 4),
            modified_timestamp=safe_get(item_data, -1, "72930366", 2, 9),
            timestamp_range=[
                safe_get(item_data, -1, "72930366", 2, 5),
                safe_get(item_data, -1, "72930366", 2, 6),
            ],
            is_shared=safe_get(item_data, -1, "72930366", 4) or False,
        )


@dataclass
class ItemInfoExt:
    media_key: Optional[str]
    dedup_key: Optional[str]
    description_full: Optional[str]
    file_name: Optional[str]
    timestamp: Optional[int]
    timezone_offset: Optional[int]
    size: Optional[int]
    res_width: Optional[int]
    res_height: Optional[int]
    camera_info: Optional[str | int]
    albums: list[Album]
    source: list[Optional[str]]
    space_taken: Optional[int]
    is_original_quality: Optional[bool]
    saved_to_your_photos: bool
    owner: Optional[Actor]
    geo_location: Optional[GeoLocation]
    other: Optional[str]

    @classmethod
    def from_data(cls, item_data):
        source = []

        source_map = {
            1: "mobile",
            2: "web",
            3: "shared",
            4: "partnerShared",
            7: "drive",
            8: "pc",
            11: "gmail",
        }

        source_secondary_map = {
            1: "android",
            3: "ios",
        }

        source.append(source_map.get(safe_get(item_data, 0, 27, 0)))
        source.append(source_secondary_map.get(safe_get(item_data, 0, 27, 1, 2)))

        owner = None
        if safe_get(item_data, 0, 27):
            owner = Actor.from_data(safe_get(item_data, 0, 27, 3, 0) or safe_get(item_data, 0, 27, 4, 0))
        if not owner or not owner.actor_id:
            owner = Actor.from_data(safe_get(item_data, 0, 28))

        return cls(
            media_key=safe_get(item_data, 0, 0),
            dedup_key=safe_get(item_data, 0, 11),
            description_full=safe_get(item_data, 0, 1),
            file_name=safe_get(item_data, 0, 2),
            timestamp=safe_get(item_data, 0, 3),
            timezone_offset=safe_get(item_data, 0, 4),
            size=safe_get(item_data, 0, 5),
            res_width=safe_get(item_data, 0, 6),
            res_height=safe_get(item_data, 0, 7),
            camera_info=safe_get(item_data, 0, 23),
            albums=[Album.from_data(album_data) for album_data in safe_get(item_data, 0, 19) or []],
            source=source,
            space_taken=safe_get(item_data, 0, 30, 1),
            is_original_quality=safe_get(item_data, 0, 30, 2) == 2,
            saved_to_your_photos=len([sub_array for sub_array in safe_get(item_data, 0, 12, default=[]) if 20 in sub_array]) == 0,
            owner=owner,
            geo_location=GeoLocation.from_data(item_data),
            other=safe_get(item_data, 0, 31),
        )


@dataclass
class ItemInfoBatch:
    media_key: str
    description_full: str
    file_name: str
    timestamp: int
    timezone_offset: int
    creation_timestamp: int
    size: int
    space_taken: int
    is_original_quality: bool

    @classmethod
    def from_data(cls, item_data):
        return cls(
            media_key=safe_get(item_data, 0),
            description_full=safe_get(item_data, 1, 2),
            file_name=safe_get(item_data, 1, 3),
            timestamp=safe_get(item_data, 1, 6),
            timezone_offset=safe_get(item_data, 1, 7),
            creation_timestamp=safe_get(item_data, 1, 8),
            size=safe_get(item_data, 1, 9),
            space_taken=safe_get(item_data, 1, -1, 1),
            is_original_quality=safe_get(item_data, 1, -1, 2) == 2,
        )


def parse_response_data(rpc_id: str, data: dict):
    match rpc_id:
        case "lcxiM":
            return LibraryTimelinePage.from_data(data)
        case "EzkLib":
            return LibraryGenericPage.from_data(data)
        case "swbisb":
            return [RemoteMatch.from_data(item) for item in safe_get(data, 0) or []]
        case "VrseUb":
            return ItemInfo.from_data(data)
        case "fDcn4b":
            return ItemInfoExt.from_data(data)
        case "EWgK9e":
            return [ItemInfoBatch.from_data(item) for item in safe_get(data, 0, 1) or []]

        case _:
            return {}
