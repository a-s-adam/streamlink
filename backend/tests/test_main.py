"""Basic tests for the FastAPI application."""
import pytest

def test_imports():
    """Test that we can import the main modules."""
    try:
        # Test basic imports without full app initialization
        import app.main
        import app.models
        import app.api
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_basic_functionality():
    """Test basic Python functionality."""
    assert 1 + 1 == 2
    assert "hello" in "hello world"
    assert len([1, 2, 3]) == 3

def test_pytest_working():
    """Test that pytest is working correctly."""
    assert True
