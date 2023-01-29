import unicodedata


def prepare_slug(title: str) -> str:
    processed_title = unicodedata.normalize(
        "NFD", title).encode("ascii", "ignore").decode("utf-8")

    slug = processed_title.replace(" ", "-").replace("_", "-").lower()

    return slug