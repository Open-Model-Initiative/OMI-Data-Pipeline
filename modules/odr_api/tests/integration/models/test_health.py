# SPDX-License-Identifier: Apache-2.0
import requests
import argparse
import sys


def test_health_check(base_url):
    """
    Test the health check endpoint of the API.

    This test performs the following checks:
    1. Sends a GET request to the '/health' endpoint.
    2. Verifies that the response status code is 200 (OK).
    3. Confirms that the response body contains the expected JSON data.

    Args:
        base_url (str): The base URL of the API, including protocol, host, and port.

    Raises:
        AssertionError: If any of the assertions fail, indicating a problem with the health check endpoint.
    """
    try:
        # Send a GET request to the health endpoint
        response = requests.get(f"{base_url}/health")

        # Check if the status code is 200 (OK)
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        # Verify the response body contains the expected data
        expected_response = {"status": "OK"}
        assert response.json() == expected_response, f"Expected response {expected_response}, but got {response.json()}"

        # If all assertions pass, the test is successful
        print("Health check test passed successfully")
        return True
    except AssertionError as e:
        print(f"Health check test failed: {str(e)}")
        return False
    except requests.RequestException as e:
        print(f"Error connecting to the API: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run health check test")
    parser.add_argument("--host", default="localhost", help="API host")
    parser.add_argument("--port", default="31100", help="API port")
    args = parser.parse_args()

    base_url = f"http://{args.host}:{args.port}/api/v1"
    success = test_health_check(base_url)
    sys.exit(0 if success else 1)
