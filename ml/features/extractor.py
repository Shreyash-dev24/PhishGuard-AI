"""
PhishGuard AI
URL Feature Extractor

This file is the single source of truth for URL feature extraction.

IMPORTANT:
- We NEVER visit or fetch the submitted URL.
- We only analyze the URL string.
- The same extractor will be used during training and prediction.
"""

import ipaddress
import re
from urllib.parse import urlsplit


# ============================================================
# 1. THE 27 FEATURES
# ============================================================

FEATURE_NAMES = [
    "url_length",
    "hostname_length",
    "path_length",
    "query_length",
    "num_dots",
    "num_hyphens",
    "num_underscores",
    "num_slashes",
    "num_question_marks",
    "num_equal_signs",
    "num_ampersands",
    "num_percent_signs",
    "num_digits",
    "num_special_chars",
    "num_subdirectories",
    "num_query_params",
    "uses_https",
    "has_ip_address",
    "has_at_symbol",
    "has_suspicious_encoding",
    "has_port",
    "is_shortened_url",
    "has_login_word",
    "has_account_word",
    "has_verification_word",
    "has_security_word",
    "num_suspicious_keywords",
]


# ============================================================
# 2. SUSPICIOUS KEYWORDS
# ============================================================

SUSPICIOUS_KEYWORDS = [
    "login",
    "signin",
    "verify",
    "verification",
    "account",
    "secure",
    "security",
    "update",
    "confirm",
    "bank",
    "payment",
    "password",
    "credential",
    "wallet",
    "bonus",
    "free",
    "claim",
]


# ============================================================
# 3. KNOWN URL SHORTENERS
# ============================================================

SHORTENED_URL_HOSTS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "buff.ly",
    "ow.ly",
    "shorturl.at",
    "cutt.ly",
    "rebrand.ly",
    "tiny.cc",
    "lnkd.in",
}


# ============================================================
# 4. NORMALIZE URL
# ============================================================

def normalize_url(url: str) -> str:
    """
    Prepare a URL for parsing.

    If the URL has no scheme, temporarily add http://.

    Example:
        example.com/login
    becomes:
        http://example.com/login

    No network request is made.
    """

    if not isinstance(url, str):
        raise TypeError("URL must be a string.")

    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    # Add a scheme if missing
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url):
        url = "http://" + url

    return url


# ============================================================
# 5. CHECK IP ADDRESS
# ============================================================

def is_ip_address(hostname: str) -> int:
    """
    Check whether the hostname is an IPv4 or IPv6 address.

    Returns:
        1 -> IP address
        0 -> normal hostname
    """

    if not hostname:
        return 0

    try:
        ipaddress.ip_address(hostname)
        return 1
    except ValueError:
        return 0


# ============================================================
# 6. COUNT QUERY PARAMETERS
# ============================================================

def count_query_params(query: str) -> int:
    """
    Count query parameters.

    Example:
        ?user=abc&id=10&verify=true

    returns:
        3
    """

    if not query:
        return 0

    return len([
        item
        for item in query.split("&")
        if item
    ])


# ============================================================
# 7. COUNT SUBDIRECTORIES
# ============================================================

def count_subdirectories(path: str) -> int:
    """
    Count subdirectories in the URL path.

    Example:
        /login/account/verify

    returns:
        2
    """

    if not path or path == "/":
        return 0

    clean_path = path.strip("/")

    if not clean_path:
        return 0

    parts = [
        part
        for part in clean_path.split("/")
        if part
    ]

    if len(parts) <= 1:
        return 0

    return len(parts) - 1


# ============================================================
# 8. SUSPICIOUS ENCODING
# ============================================================

def has_suspicious_encoding(url: str) -> int:
    """
    Detect percent-encoded characters.

    Examples:
        %20
        %2F
        %40
        %3D
        %3F
        %26
    """

    pattern = r"%[0-9a-fA-F]{2}"

    return int(bool(re.search(pattern, url)))


# ============================================================
# 9. CHECK EXPLICIT PORT
# ============================================================

def has_port(parsed_url) -> int:
    """
    Check whether the URL contains an explicit port.

    Example:
        example.com:8080
    """

    try:
        return int(parsed_url.port is not None)
    except ValueError:
        return 0


# ============================================================
# 10. CHECK URL SHORTENER
# ============================================================

def is_shortened_url(hostname: str) -> int:
    """
    Check whether the hostname belongs to a known
    URL-shortening service.
    """

    if not hostname:
        return 0

    hostname = hostname.lower().strip(".")

    return int(hostname in SHORTENED_URL_HOSTS)


# ============================================================
# 11. MAIN FEATURE EXTRACTION FUNCTION
# ============================================================

def extract_url_features(url: str) -> dict:
    """
    Extract exactly 27 features from a URL.

    Returns:
        Dictionary containing the 27 features.
    """

    # Normalize URL
    normalized_url = normalize_url(url)

    # Parse URL
    parsed = urlsplit(normalized_url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    url_lower = normalized_url.lower()

    # --------------------------------------------------------
    # Basic character counts
    # --------------------------------------------------------

    num_digits = sum(
        char.isdigit()
        for char in normalized_url
    )

    num_special_chars = sum(
        not char.isalnum()
        for char in normalized_url
    )

    # --------------------------------------------------------
    # Suspicious words
    # --------------------------------------------------------

    has_login_word = int(
        "login" in url_lower
        or "signin" in url_lower
    )

    has_account_word = int(
        "account" in url_lower
    )

    has_verification_word = int(
        "verify" in url_lower
        or "verification" in url_lower
        or "confirm" in url_lower
    )

    has_security_word = int(
        "secure" in url_lower
        or "security" in url_lower
    )

    num_suspicious_keywords = sum(
        word in url_lower
        for word in SUSPICIOUS_KEYWORDS
    )

    # --------------------------------------------------------
    # Create the feature dictionary
    # --------------------------------------------------------

    features = {

        "url_length":
            len(normalized_url),

        "hostname_length":
            len(hostname),

        "path_length":
            len(path),

        "query_length":
            len(query),

        "num_dots":
            normalized_url.count("."),

        "num_hyphens":
            normalized_url.count("-"),

        "num_underscores":
            normalized_url.count("_"),

        "num_slashes":
            normalized_url.count("/"),

        "num_question_marks":
            normalized_url.count("?"),

        "num_equal_signs":
            normalized_url.count("="),

        "num_ampersands":
            normalized_url.count("&"),

        "num_percent_signs":
            normalized_url.count("%"),

        "num_digits":
            num_digits,

        "num_special_chars":
            num_special_chars,

        "num_subdirectories":
            count_subdirectories(path),

        "num_query_params":
            count_query_params(query),

        "uses_https":
            int(parsed.scheme.lower() == "https"),

        "has_ip_address":
            is_ip_address(hostname),

        "has_at_symbol":
            int("@" in normalized_url),

        "has_suspicious_encoding":
            has_suspicious_encoding(normalized_url),

        "has_port":
            has_port(parsed),

        "is_shortened_url":
            is_shortened_url(hostname),

        "has_login_word":
            has_login_word,

        "has_account_word":
            has_account_word,

        "has_verification_word":
            has_verification_word,

        "has_security_word":
            has_security_word,

        "num_suspicious_keywords":
            num_suspicious_keywords,
    }

    # --------------------------------------------------------
    # Make sure we ALWAYS have exactly 27 features
    # --------------------------------------------------------

    if list(features.keys()) != FEATURE_NAMES:
        raise RuntimeError(
            "Feature schema mismatch. "
            "Expected exactly 27 features."
        )

    return features


# ============================================================
# 12. RETURN FEATURES AS ML VECTOR
# ============================================================

def extract_feature_vector(url: str) -> list:
    """
    Convert the feature dictionary into an ordered list.

    This format will be used by Random Forest and ANN.
    """

    features = extract_url_features(url)

    return [
        features[name]
        for name in FEATURE_NAMES
    ]


# ============================================================
# 13. TEST THE EXTRACTOR
# ============================================================

if __name__ == "__main__":

    test_urls = [
        "https://www.google.com/",
        "http://example.com/login",
        "http://192.168.1.10/verify/account",
        "https://bit.ly/abc123",
    ]

    for url in test_urls:

        print("\n" + "=" * 60)

        print("URL:", url)

        features = extract_url_features(url)

        print(
            "Number of features:",
            len(features)
        )

        for name, value in features.items():

            print(
                f"{name}: {value}"
            )
            
    def extract_features(url):
        return extract_feature_vector(url)