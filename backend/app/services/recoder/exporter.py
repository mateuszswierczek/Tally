from app.services.analyzer.frequencies import generate_frequencies_table
from app.services.recoder.schema import Question


import pandas as pd
import zipfile
import tempfile
import pyreadstat
import io
import os
import re

STARTCOL:int = 1
BUFFER:int = 2

def write_to_excel(decoded:pd.DataFrame, encodec:pd.DataFrame, mapping:list[Question], book_of_codes:pd.DataFrame) -> io.BytesIO:
    buffer = io.BytesIO()
    startrow = 0

    with zipfile.ZipFile(buffer, "w") as zf:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(path=excel_buffer, engine="openpyxl") as writer:
            decoded.to_excel(writer, sheet_name="Baza rozkodowana", index=False)
            encodec.to_excel(writer, sheet_name="Baza zakodowana", index=False)
            book_of_codes.to_excel(writer, sheet_name="Księga kodów", index=False)
            frequencies_tables = generate_frequencies_table(mapping)
            for frequencies_table in frequencies_tables:
                frequencies_table.to_excel(writer, 
                                           startcol=STARTCOL,
                                           startrow=startrow,
                                           sheet_name="Częstości", 
                                           index=False)    
                startrow += frequencies_table.shape[0] + BUFFER  

        spss_file = write_to_spss(decoded, mapping)
        zf.writestr("Baza danych.xlsx", excel_buffer.getvalue())
        zf.writestr("Baza danych.sav", spss_file.getvalue())

    buffer.seek(0)
    return buffer

#TODO: Księga kodów
#TODO: Przepisać na klasę
def write_to_spss(decoded:pd.DataFrame, encodec:list) -> io.BytesIO:
    tmp_path = open_tempfile()
    buffer = io.BytesIO()
    try:
        decoded.columns = [sanitize_name(col) for col in decoded.columns]
        variable_labels = parser_variable_labels(encodec)
        buffer = write_sav_to_tempfile(decoded, tmp_path, variable_labels)
    finally:
        os.remove(tmp_path)
    
    buffer.seek(0)
    return buffer 

def parser_variable_labels(encodec:list) -> dict:
    temp = {}
    for col in encodec:
        if col.type == "continuous":
            continue
        if col.type == "text":
            continue
        if col.cafeteria is None:
            continue
        question_sanitized = sanitize_name(col.question)
        temp[question_sanitized] =  {c.index: c.value for c in col.cafeteria}
    return temp


def write_frequencies_tables_to_excel(mapping):
    pass

def write_sav_to_tempfile(decoded:pd.DataFrame, tmp_path:str, variable_labels:dict) -> io.BytesIO:
    pyreadstat.write_sav(decoded, tmp_path, variable_value_labels=variable_labels)
    with open(tmp_path, "rb") as f:
        buffer = io.BytesIO(f.read())
    return buffer

def open_tempfile() -> str:
    tmp_path = None
    with tempfile.NamedTemporaryFile(suffix='.sav', delete=False) as f:
        tmp_path = f.name
    return tmp_path

def sanitize_name(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-zA-Z0-9_@#$]", "_", name)
    if name and name[0].isdigit():
        name = "_" + name
    return name[:64]

