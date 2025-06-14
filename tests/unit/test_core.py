from app.core import generate_short_code

def test_generate_short_code():
    code = generate_short_code()
    assert isinstance(code, str)
    assert len(code) == 6