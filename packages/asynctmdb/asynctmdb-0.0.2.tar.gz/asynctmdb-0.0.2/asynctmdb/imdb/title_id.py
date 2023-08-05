LENGTH = 7


def from_int(int_id: int,
             *,
             length: int = LENGTH) -> str:
    """Convert integer IMDb id to string representation."""
    return 'tt{int_id:0>{length}}'.format(int_id=int_id,
                                          length=length)
