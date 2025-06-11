import sys
import hashlib


# Hashing con salt (para contraseñas)
def hash_password(password: str):
    hashed = hashlib.sha256()
    hashed.update(password.encode(encoding="utf-8"))
    return hashed.hexdigest()


args = sys.argv[1:]

kwargs = {}

for idx, arg in enumerate(args):
    if arg.startswith("--"):
        kwargs[arg[2:]] = args[idx + 1]


if not kwargs["password"]:
    print("Debe de pasar el parametro --password")
    sys.exit(-1)

print(hash_password(kwargs["password"]))
