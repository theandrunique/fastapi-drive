def get_file_category(mime_type: str) -> str:
    if mime_type.startswith("audio"):
        return "audio"
    elif mime_type.startswith("video"):
        return "video"
    elif mime_type.startswith("image"):
        return "image"
    else:
        return "file"
