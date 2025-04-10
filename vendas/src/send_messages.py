import requests
from requests.exceptions import RequestException

def _send_message(
    url_with_route: str,
    token: str,
    message_data: dict[str, str],
    required_key: str,
    endpoint_suffix: str
) -> None:
    if not url_with_route.endswith(endpoint_suffix):
        raise ValueError(f"URL must end with '{endpoint_suffix}'")

    if required_key not in message_data:
        raise ValueError(f"message_data must contain '{required_key}'")

    data = {
        "phone": message_data["phone"],
        required_key: message_data[required_key]
    }

    headers = {"Client-Token": token}

    try:
        response = requests.post(url_with_route, data=data, headers=headers, timeout=15)
        response.raise_for_status()
    except RequestException as e:
        raise RequestException(f"Failed to send message to {message_data['phone']}: {str(e)}")

def send_text(url: str, token: str, message_data: dict[str, str]) -> None:
    url_with_route = url + "/send-text"
    _send_message(url_with_route, token, message_data, "message", "send-text")

def send_audio(url: str, token: str, message_data: dict[str, str]) -> None:
    url_with_route = url + "send-audio"
    _send_message(url_with_route, token, message_data, "audio", "send-audio")
