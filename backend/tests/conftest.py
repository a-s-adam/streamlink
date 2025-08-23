"""Test configuration and fixtures."""
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "user_id": "test-user-123",
        "item_title": "Test Movie",
        "source": "NETFLIX"
    }

@pytest.fixture
def mock_response():
    """Provide mock API response data."""
    return {
        "status": "success",
        "message": "Test completed successfully"
    }
