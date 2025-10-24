from fastapi import HTTPException, status


async def validate_id(id: int) -> int:
    if not isinstance(id, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="id must be an integer"
        )
    elif id == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="id cannot be equal 0"
        )
    elif id < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="id cannot less than 0"
        )

    return id
