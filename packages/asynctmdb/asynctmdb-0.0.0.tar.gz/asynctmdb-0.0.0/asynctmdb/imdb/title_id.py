LENGTH = 7


def from_int(int_id: int) -> str:
    return f'tt{int_id:0>{LENGTH}}'
