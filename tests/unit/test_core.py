import pytest
from app.core import generate_short_link

def test_generate_short_link_length():
    short = generate_short_link()
    assert isinstance(short, str)
    assert len(short) == 6  # как в реализации

def test_generate_short_link_uniqueness():
    results = {generate_short_link() for _ in range(1000)}
    assert len(results) == 1000
