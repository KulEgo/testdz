import pytest
from app.core import generate_short_code

def test_generate_short_code_length():
    code = generate_short_code()
    assert isinstance(code, str)
    assert len(code) == 6  # обычно 6 символов, проверь в коде core.py

def test_generate_short_code_uniqueness():
    codes = {generate_short_code() for _ in range(1000)}
    assert len(codes) == 1000
