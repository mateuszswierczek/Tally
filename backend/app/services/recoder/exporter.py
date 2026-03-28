import pandas as pd
import zipfile
import io

def write_to_excel(decoded:pd.DataFrame, encodec:pd.DataFrame):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w") as zf:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(path=excel_buffer, engine="openpyxl") as writer:
            decoded.to_excel(writer, sheet_name="Baza rozkodowana", index=False)
            encodec.to_excel(writer, sheet_name="Baza zakodowana", index=False)
        zf.writestr("Baza danych.xlsx", excel_buffer.getvalue())

    buffer.seek(0)
    return buffer
