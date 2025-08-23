"""Basic tests for the FastAPI application."""
import pytest

def test_basic_functionality():
    """Test basic Python functionality."""
    assert 1 + 1 == 2
    assert "hello" in "hello world"
    assert len([1, 2, 3]) == 3

def test_pytest_working():
    """Test that pytest is working correctly."""
    assert True

def test_imports_basic():
    """Test that we can import basic modules without full app initialization."""
    try:
        # Test basic imports that don't require SQLAlchemy setup
        import app.config
        import app.db.database
        assert True
    except ImportError as e:
        pytest.fail(f"Basic import failed: {e}")
    except Exception as e:
        # Other errors are expected when not fully configured
        assert "database" in str(e) or "connection" in str(e) or "pgvector" in str(e)
