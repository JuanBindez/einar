def key_len(key: bytes, as_bytes: bool = False) -> int:
    """
    Returns the key length in bytes or bits.

    :param key: Key to calculate the length.
    :param as_bytes: If True, returns the length in bytes; if False, in bits.
    :return: Key length in bytes or bits.
    """

    if as_bytes:
        return len(key)
    else:
        return len(key) * 8