from api_tests.search_helper import invoke_search_api
from api_tests.logger import get_logger
import pytest
logger = get_logger()

def get_upload_time():
    with open("upload_time.txt", "r") as f:
        return int(f.read().strip())


org = "default"
stream = "default"
end_time = get_upload_time()
start_time = end_time - (60 * 1_000_000)  # 1 minute before

@pytest.mark.parametrize("size,condition",[(10,"stream!='stderr'" )])
def test_validate_size_with_no_errors(size,condition):
    # size=30
    logger.info(f" Test - Validating the response with {condition} and Top {size} records")
    # condition = "stream!='stderr'"   
    logger.info(f"--- Invoking Search API ---")
    response = invoke_search_api(org, stream, condition, start_time, end_time,size)

    assert response.status_code == 200, "Expected status code 200"
    response_json = response.json()
    logger.info(f"The Response status code found was : {response.status_code}")
    logger.info(f"Got Non Empty response with {len(response_json.get('hits', []))} records")

    #  Assert 1: number of records returned matches "size" 
    results = response_json.get("hits", [])
    result_count = len(results)
    assert result_count == size, f"Expected at most {size} results, got {result_count}"
    logger.info(f" Result count is as expected : {result_count}")

    #  Assert 2: each record satisfies the condition "stream != 'stderr'"
    passed_records = 0
    for idx, record in enumerate(results):
        stream_value = record.get("stream")
        assert stream_value != "stderr", f"Found record with stream='stderr': {record}"
        logger.info(f"Record {idx+1} passed stream check: stream='{stream_value}'")
        passed_records += 1

    logger.info(f" All {passed_records} records satisfy the condition: stream != 'stderr'")


 