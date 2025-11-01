import secrets


def generate_verification_key() -> str:
    """Random 5 number key"""
    return "".join(secrets.choice("0123456789") for _ in range(5))
