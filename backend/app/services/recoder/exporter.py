import pandas as pd
import zipfile
import tempfile
import pyreadstat
import io
import os
import re

from app.services.analyzer.schema import FrequencieTable, MAQTable, MatrixTable, Crosstable
from app.services.analyzer.analyzer import Analyzer
from app.services.recoder.schema import Question

STARTCOL:int = 1
STARTCOL_PERCENTAGE:int = 8
BUFFER:int = 2
CROSSTABLE_BUFFER:int = 2

def write_to_excel(analyzer:Analyzer, decoded:pd.DataFrame, encodec:pd.DataFrame, mapping:list[Question], book_of_codes:pd.DataFrame) -> io.BytesIO:
    buffer = io.BytesIO()
    startrow = 0
    analyzer.create_frequencies_tables()
    analyzer.generate_crosstable()
    frequencies_tables:list[FrequencieTable | MAQTable | MatrixTable] = analyzer.tables
    cross_tables:list[Crosstable] = analyzer.crosstable_tables

    with zipfile.ZipFile(buffer, "w") as zf:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(path=excel_buffer, engine="openpyxl") as writer:
            decoded.to_excel(writer, sheet_name="Baza rozkodowana", index=False, na_rep="999")
            encodec.to_excel(writer, sheet_name="Baza zakodowana", index=False, na_rep="999")
            book_of_codes.to_excel(writer, sheet_name="Księga kodów", index=False)
            for table in frequencies_tables:
                table.combined_table.to_excel(writer, 
                                           startcol=STARTCOL,
                                           startrow=startrow,
                                           sheet_name="Częstości") 
                table.percentage_table.to_excel(writer, 
                                           startcol=STARTCOL_PERCENTAGE if table.combined_table.shape[1] < STARTCOL_PERCENTAGE else table.combined_table.shape[1] + 1 + BUFFER,
                                           startrow=startrow,
                                           sheet_name="Częstości") 
                startrow += table.frequncie_table.shape[0] + 1 + BUFFER
            startrow = 0
            for crosstable in cross_tables:
                crosstable.combined_table.to_excel(writer, 
                                           startcol=STARTCOL,
                                           startrow=startrow,
                                           sheet_name="Krzyżówki")
                startrow += crosstable.combined_table.shape[0] + 1 + BUFFER
        spss_file = write_to_spss(decoded, mapping)
        zf.writestr("Baza danych.xlsx", excel_buffer.getvalue())
        zf.writestr("Baza danych.sav", spss_file.getvalue())

    buffer.seek(0)
    return buffer

def write_to_spss(decoded:pd.DataFrame, encodec:list) -> io.BytesIO:
    tmp_path = open_tempfile()
    try:
        new_columns = [sanitize_name(col) for col in decoded.columns]
        unique_cols = []
        counts = {}
        
        for col in new_columns:
            if col not in counts:
                unique_cols.append(col)
                counts[col] = 1
            else:
                new_name = f"{col}_{counts[col]}"
                unique_cols.append(new_name)
                counts[col] += 1
        decoded.columns = unique_cols
        variable_labels = parser_variable_labels(encodec)
        buffer = write_sav_to_tempfile(decoded, tmp_path, variable_labels)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    buffer.seek(0)
    return buffer

def open_tempfile() -> str:
    tmp_path = None
    with tempfile.NamedTemporaryFile(suffix='.sav', delete=False) as f:
        tmp_path = f.name
    return tmp_path

def sanitize_name(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name)
    if not name or not name[0].isalpha():
        name = "V" + name
    return name[:60]

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

def write_sav_to_tempfile(decoded:pd.DataFrame, tmp_path:str, variable_labels:dict) -> io.BytesIO:
    pyreadstat.write_sav(decoded, tmp_path, variable_value_labels=variable_labels)
    with open(tmp_path, "rb") as f:
        buffer = io.BytesIO(f.read())
    return buffer