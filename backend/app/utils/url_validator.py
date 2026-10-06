from urllib.parse import urlsplit


# --------------------------------------------------
# URL Validation
# --------------------------------------------------

def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate a URL for static phishing analysis.

    This function only parses the URL string.
    It does NOT make any network request.
    """

    # Basic type check
    if not isinstance(url, str):
        return False, "URL must be a string."

    # Remove accidental spaces around the URL
    url = url.strip()

    # Empty URL
    if not url:
        return False, "URL cannot be empty."

    # Prevent whitespace inside the URL
    if any(character.isspace() for character in url):
        return False, "URL cannot contain spaces."

    # URL length protection
    if len(url) > 2048:
        return False, "URL is too long. Maximum length is 2048 characters."

    # A valid web URL must use HTTP or HTTPS
    if not (
        url.lower().startswith("http://")
        or url.lower().startswith("https://")
    ):
        return False, "URL must start with http:// or https://."

    # Parse the URL without contacting it
    try:
        parsed = urlsplit(url)
    except ValueError:
        return False, "Invalid URL format."

    # Scheme check
    if parsed.scheme.lower() not in {"http", "https"}:
        return False, "Only HTTP and HTTPS URLs are supported."

    # Hostname check
    try:
        hostname = parsed.hostname
    except ValueError:
        return False, "Invalid hostname."

    if not hostname:
        return False, "URL must contain a hostname."

    # Validate port syntax if a port is present
    try:
        _ = parsed.port
    except ValueError:
        return False, "Invalid port number."

    return True, ""