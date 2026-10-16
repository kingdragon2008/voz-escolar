import secrets


def generate_protocol_number(prefix: str = "PRT-2026", length: int = 5) -> str:
    """
    Gera um protocolo pseudoaleatório para rastreio ético do aluno.
    Exemplo: PRT-2026-98X2F
    """
    allowed_chars = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
    suffix = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    return f"{prefix}-{suffix}"
