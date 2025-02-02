from dataclasses import dataclass, field, fields
from typing import List, Optional, Any
from .utils import jpath


@dataclass
class GeoLocation:
    coordinates: Optional[list] = None
    name: Optional[str] = None

    @classmethod
    def from_data(cls, data):
        return cls(coordinates=jpath(data, "$[1][0]"), name=jpath(data, "$[1][4][0][1][0][0]"))


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
    descriptionShort: Optional[str]
    is_live_photo: bool
    live_photo_duration: Optional[int]
    is_owned: bool
    geo_location: GeoLocation

    @classmethod
    def from_data(cls, item_data):
        return cls(
            media_key=jpath(item_data, "$[0]"),
            timestamp=jpath(item_data, "$[2]"),
            timezone_offset=jpath(item_data, "$[4]"),
            creation_timestamp=jpath(item_data, "$[5]"),
            dedup_key=jpath(item_data, "$[3]"),
            thumbnail_url=jpath(item_data, "$[1][0]"),
            res_width=jpath(item_data, "$[1][1]"),
            res_height=jpath(item_data, "$[1][2]"),
            is_partial_upload=jpath(item_data, "$[12][0]") == 20,
            is_archived=jpath(item_data, "$[13]"),
            is_favorite=jpath(item_data, "$[-1]['163238866'][0]"),
            video_duration=jpath(item_data, "$[-1]['76647426'][0]"),
            descriptionShort=jpath(item_data, "$[-1]['396644657'][0]"),
            is_live_photo=jpath(item_data, "$[-1]['146008172']") is not None,
            live_photo_duration=jpath(item_data, "$[-1]['146008172'][1]"),
            is_owned=all(27 not in sub for sub in jpath(item_data, "$[7]")),
            geo_location=GeoLocation.from_data(jpath(item_data, "$[-1]['129168200']") or {}),
        )


@dataclass
class LibraryTimelinePage:
    items: List[LibraryItem]
    nextPageId: Optional[str]
    lastItemTimestamp: Optional[int]

    @classmethod
    def from_data(cls, data):
        return cls(items=[LibraryItem.from_data(item) for item in jpath(data, "$[0]") or []], nextPageId=jpath(data, "$[1]"), lastItemTimestamp=int(jpath(data, "$[2]")) if jpath(data, "$[2]") is not None else None)


@dataclass
class LibraryGenericPage:
    items: List[LibraryItem]
    nextPageId: Optional[str]

    @classmethod
    def from_data(cls, data):
        return cls(items=[LibraryItem.from_data(item) for item in jpath(data, "$[0]") or []], nextPageId=jpath(data, "$[1]"))


@dataclass
class BaseDataClass:
    """Base class for dataclasses that parse data using jpath."""

    @classmethod
    def get_jpath_value(cls, data: dict[Any, Any], path: str) -> Optional[Any]:
        """Retrieve a value from a nested dictionary using a jpath expression."""
        try:
            return jpath(data, path)
        except Exception as e:
            raise ValueError(f"Error accessing path '{path}': {e}")

    @classmethod
    def from_data(cls, item_data: dict[Any, Any]):
        """Create an instance of the dataclass by parsing data using jpath paths specified in metadata."""
        init_args = {}
        errors = []

        for _field in fields(cls):
            jpath_expr = _field.metadata.get("jpath")
            if jpath_expr:
                try:
                    value = cls.get_jpath_value(item_data, jpath_expr)
                    init_args[_field.name] = value
                except ValueError as e:
                    # Collect errors for better debugging
                    errors.append(f"Field '{_field.name}' failed with error: {e}")
                    init_args[_field.name] = None  # Optionally set a default value

        if errors:
            raise ValueError("Failed to parse the following fields:\n" + "\n".join(errors))

        return cls(**init_args)


@dataclass
class RemoteMatch(BaseDataClass):
    hash: str = field(metadata={"jpath": "$[0]"})
    media_key: str = field(metadata={"jpath": "$[1][0]"})
    thumbnail_url: str = field(metadata={"jpath": "$[1][1][0]"})
    res_width: int = field(metadata={"jpath": "$[1][1][1]"})
    res_height: int = field(metadata={"jpath": "$[1][1][2]"})
    timestamp: int = field(metadata={"jpath": "$[1][2]"})
    dedup_key: str = field(metadata={"jpath": "$[1][3]"})
    timezone_offset: int = field(metadata={"jpath": "$[1][4]"})
    creation_timestamp: int = field(metadata={"jpath": "$[1][5]"})
    video_duration: Optional[int] = field(metadata={"jpath": "$[1][-1]['76647426'][0]"})
    camera_info: Optional[dict] = field(metadata={"jpath": "$[1][1][8]"})


def parse_resonse_data(rpc_id: str, data: dict):
    match rpc_id:
        case "lcxiM":
            return LibraryTimelinePage.from_data(data)
        case "EzkLib":
            return LibraryGenericPage.from_data(data)
        case "swbisb":
            return [RemoteMatch.from_data(item) for item in jpath(data, "$[0]") or []]
        case _:
            return {}
