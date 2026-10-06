from backend.app.utils.url_validator import validate_url


def test_valid_https_url():
    valid, message = validate_url(
        "https://www.google.com/"
    )

    assert valid is True
    assert message == ""


def test_valid_http_url():
    valid, message = validate_url(
        "http://192.168.1.10/login"
    )

    assert valid is True
    assert message == ""


def test_valid_url_with_query():
    valid, message = validate_url(
        "https://example.com/login?user=test&id=123"
    )

    assert valid is True
    assert message == ""


def test_empty_url():
    valid, message = validate_url("")

    assert valid is False
    assert "empty" in message.lower()


def test_url_without_http_scheme():
    valid, message = validate_url(
        "www.google.com"
    )

    assert valid is False
    assert "http" in message.lower()


def test_url_with_spaces():
    valid, message = validate_url(
        "https://example.com/login page"
    )

    assert valid is False
    assert "spaces" in message.lower()


def test_missing_hostname():
    valid, message = validate_url(
        "https://"
    )

    assert valid is False
    assert "hostname" in message.lower()


def test_invalid_port():
    valid, message = validate_url(
        "https://example.com:abc/"
    )

    assert valid is False
    assert "port" in message.lower()