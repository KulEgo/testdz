import hashlib

def generate_short_code(url: str) -> str:
    # Простая функция генерации кода — взять первые 6 символов md5
    m = hashlib.md5()
    m.update(url.encode('utf-8'))
    return m.hexdigest()[:6]
