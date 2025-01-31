from .utils import get_nested


# NOTE add =w417-h174-k-no?authuser=0 to thumbnail url to set custon size, remove 'video' watermark, remove auth requirement


def library_item_parse(item_data):
    # Determine isOwned by checking if item_data[7] has any sub-array containing 27.
    sub_arrays = get_nested(item_data, 7, default=[])
    if not isinstance(sub_arrays, list):
        sub_arrays = []
    is_owned = all(27 not in sub for sub in sub_arrays if isinstance(sub, list))

    return {
        "mediaKey": get_nested(item_data, 0),
        "timestamp": get_nested(item_data, 2),
        "timezoneOffset": get_nested(item_data, 4),
        "creationTimestamp": get_nested(item_data, 5),
        "dedupKey": get_nested(item_data, 3),
        "thumb": get_nested(item_data, 1, 0) + "?authuser=0",
        "resWidth": get_nested(item_data, 1, 1),
        "resHeight": get_nested(item_data, 1, 2),
        "isPartialUpload": get_nested(item_data, 12, 0) == 20,
        "isArchived": get_nested(item_data, 13),
        "isFavorite": get_nested(item_data, -1, 163238866, 0),
        "duration": get_nested(item_data, -1, 76647426, 0),
        "descriptionShort": get_nested(item_data, -1, 396644657, 0),
        "isLivePhoto": get_nested(item_data, -1, 146008172) is not None,
        "livePhotoDuration": get_nested(item_data, -1, 146008172, 1),
        "isOwned": is_owned,
        "geoLocation": {"coordinates": get_nested(item_data, -1, 129168200, 1, 0), "name": get_nested(item_data, -1, 129168200, 1, 4, 0, 1, 0, 0)},
    }


def library_timeline_page(data):
    # Safely get the items from data[0].
    items_data = get_nested(data, 0, default=[])

    return {
        "items": [library_item_parse(item) for item in items_data],
        "nextPageId": get_nested(data, 1),
        "lastItemTimestamp": int(get_nested(data, 2)) if get_nested(data, 2) is not None else None,
    }


def parse(rpc_id: str, data: dict) -> list | dict:
    match rpc_id:
        case "lcxiM":
            return library_timeline_page(data)
        # case "nMFwOc":
        #     return locked_folder_page(data)
        # case "EzkLib":
        #     return library_generic_page(data)
        # case "F2A0H":
        #     return links_page(data)
        # case "Z5xsfc":
        #     return albums_page(data)
        # case "snAcKc":
        #     return album_items_page(data)
        # case "e9T5je":
        #     return partner_shared_items_page(data)
        # case "zy0IHe":
        #     return trash_page(data)
        # case "VrseUb":
        #     return item_info_parse(data)
        # case "fDcn4b":
        #     return item_info_ext_parse(data)
        # case "EWgK9e":
        #     return bulk_media_info(data)
        # case "dnv2s":
        #     return download_token_check_parse(data)
        # case "EzwWhf":
        #     return storage_quota_parse(data)
        # case "swbisb":
        #     return remote_matches_parse(data)
        case _:
            return {}
