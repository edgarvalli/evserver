import hashlib

# Hashing con salt (para contraseñas)
def hash_password(password: str):
    hashed = hashlib.sha256()
    hashed.update(password.encode(encoding='utf-8'))
    return hashed.hexdigest()