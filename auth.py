import hashlib


# Hash SHA-256 da senha de acesso (salt + senha).
# Para gerar um novo hash, execute em Python:
#   import hashlib; print(hashlib.sha256(("oil-gas-addon-salt" + "SUA_SENHA").encode()).hexdigest())
_PASSWORD_HASH = "2bcd412a1be32ccc8ee37437c07d6716d17050eda9af919e84547274f8bc2c79"

# Estado de autenticação em memória (por sessão do Blender)
_authenticated = False


def _hash_password(password: str) -> str:
    salt = "oil-gas-addon-salt"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def login(password: str) -> bool:
    global _authenticated
    if _hash_password(password) == _PASSWORD_HASH:
        _authenticated = True
        return True
    _authenticated = False
    return False


def logout() -> None:
    global _authenticated
    _authenticated = False


def is_authenticated() -> bool:
    return _authenticated
    #return True

