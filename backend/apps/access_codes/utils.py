import secrets
import string


def generate_single_code(prefix: str = "ESC-2026", length: int = 4) -> str:
    """
    Gera um código aleatório no formato ESC-2026-XXXX usando caracteres não ambíguos.
    Evita caracteres fáceis de confundir (0, O, 1, I, L).
    """
    allowed_chars = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
    suffix = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    return f"{prefix}-{suffix}"
