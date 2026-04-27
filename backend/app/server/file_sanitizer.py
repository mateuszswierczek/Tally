from fastapi import HTTPException, status, UploadFile

MAX_FILE_SIZE = 10 * 1024 * 1024 #10 MB

async def sanitize_excel_file(file: UploadFile):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Brak pliku."
        )
    header = await file.read(MAX_FILE_SIZE + 1)
    await file.seek(0)

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Brak nazwy pliku."
        )

    if len(header) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Plik jest za duży."
        )
    
    if not header.startswith(b'PK\x03\x04'):    
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Nieprawidłowy format pliku."
        )

    #TODO: Zastanowić się, czy to ma sens jak sprawdzamy bajty
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Zły content-type."
        )

    if not file.filename.endswith(".xlsx") and not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Złe rozszerzenie pliku."
        )