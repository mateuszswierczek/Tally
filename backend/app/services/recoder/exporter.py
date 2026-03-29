import pandas as pd
import zipfile
import tempfile
import pyreadstat
import io
import os
import re

def write_to_excel(decoded:pd.DataFrame, encodec:pd.DataFrame, mapping:list):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w") as zf:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(path=excel_buffer, engine="openpyxl") as writer:
            decoded.to_excel(writer, sheet_name="Baza rozkodowana", index=False)
            encodec.to_excel(writer, sheet_name="Baza zakodowana", index=False)
        spss_file = write_to_spss(decoded, mapping)
        zf.writestr("Baza danych.xlsx", excel_buffer.getvalue())
        zf.writestr("Baza danych.sav", spss_file.getvalue())

    buffer.seek(0)
    return buffer

def write_to_spss(decoded:pd.DataFrame, encodec:list):
    buffer = io.BytesIO()
    temp = {}
    for col in encodec:
        if col.type == "continuous":
            continue
        if col.type == "text":
            continue
        if col.cafeteria is None:
            continue
        temp[col.question] =  {c.index: c.value for c in col.cafeteria}

    with tempfile.NamedTemporaryFile(suffix=".sav", delete=False) as f:
        tmp_path = f.name

    try:
        decoded.columns = [sanitize_spss_name(col) for col in decoded.columns]
        pyreadstat.write_sav(decoded, tmp_path, variable_value_labels=temp)
        with open(tmp_path, "rb") as f:
            buffer = io.BytesIO(f.read())
    finally:
        os.remove(tmp_path)

    buffer.seek(0)
    return buffer 

def sanitize_spss_name(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-zA-Z0-9_@#$]", "_", name)
    if name and name[0].isdigit():
        name = "_" + name
    return name[:64]
