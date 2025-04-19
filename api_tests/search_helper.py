import json
import time
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from api_tests.config import BASE_URL, ZO_ROOT_USER_EMAIL, ZO_ROOT_USER_PASSWORD
from api_tests.logger import get_logger

logger = get_logger()

def invoke_search_api(org: str, stream: str, condition: str, start_time: int, end_time: int,size=10):
    url = f"{BASE_URL}/api/{org}/_search"

    payload = {
        "query": {
            "sql": f"SELECT * FROM {stream} where {condition}",
            "start_time": start_time,
            "end_time": end_time,
            "from": 0,
            "size": size
        },
        "search_type": "ui",
        "timeout": 0
    }

    try:
        response = requests.post(
            url,
            json=payload,
            auth=HTTPBasicAuth(ZO_ROOT_USER_EMAIL, ZO_ROOT_USER_PASSWORD)
        )
    except ConnectionError:
        logger.error("Failed to connect to OpenObserve server.")
        logger.error("Please make sure the OpenObserve container is running using ./infra_setup.sh")
        raise RuntimeError("OpenObserve server is not running. Start it before running tests.")

    logger.info(f"POST {url}")
    logger.info(f"Payload: {payload}")
    logger.info(f"Response code: {response.status_code}")

    return response
