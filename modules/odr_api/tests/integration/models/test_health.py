from fastapi.testclient import TestClient
from odr_api.main import app


# Create a test client using the FastAPI app
client = TestClient(app)


def test_health_check():
    """
    Test the health check endpoint of the API.

    This test performs the following checks:
    1. Sends a GET request to the '/health' endpoint.
    2. Verifies that the response status code is 200 (OK).
    3. Confirms that the response body contains the expected JSON data.

    The test ensures that the API's health check endpoint is functioning correctly,
    which is crucial for monitoring the API's availability and readiness.

    Raises:
        AssertionError: If any of the assertions fail, indicating a problem with the health check endpoint.
    """
    # Send a GET request to the health endpoint
    response = client.get("/health")

    # Check if the status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Verify the response body contains the expected data
    expected_response = {"status": "OK"}
    assert response.json() == expected_response, f"Expected response {expected_response}, but got {response.json()}"

    # If all assertions pass, the test is successful
    print("Health check test passed successfully")
