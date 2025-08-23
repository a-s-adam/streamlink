"""Simple tests that don't require database or complex imports."""
import pytest

def test_python_basics():
    """Test basic Python functionality."""
    assert True
    assert 1 + 1 == 2
    assert "test" in "this is a test"

def test_string_operations():
    """Test string operations."""
    text = "hello world"
    assert len(text) == 11
    assert text.upper() == "HELLO WORLD"
    assert text.split() == ["hello", "world"]

def test_list_operations():
    """Test list operations."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert max(numbers) == 5
    assert min(numbers) == 1

def test_dict_operations():
    """Test dictionary operations."""
    data = {"name": "test", "value": 42}
    assert data["name"] == "test"
    assert data["value"] == 42
    assert len(data) == 2
