from app.services.analyzer.frequencies import generate_frequencies_table
from app.services.analyzer.crosstables_merged import generate_crosstable_merged
from app.services.recoder.schema import Question
import pandas as pd
import zipfile
import tempfile
import pyreadstat
import io
import os
import re

STARTCOL:int = 1
STARTCOL_PERCENTAGE:int = 8
BUFFER:int = 2
CROSSTABLE_BUFFER:int = 2

def write_to_excel_merged(decoded:pd.DataFrame, encodec:pd.DataFrame, mapping:list[Question], book_of_codes:pd.DataFrame, crosstables:list[str]) -> io.BytesIO:
    buffer = io.BytesIO()
    startrow = 0

    with zipfile.ZipFile(buffer, "w") as zf:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(path=excel_buffer, engine="openpyxl") as writer:
            decoded.to_excel(writer, sheet_name="Baza rozkodowana", index=False, na_rep="999")
            encodec.to_excel(writer, sheet_name="Baza zakodowana", index=False, na_rep="999")
            book_of_codes.to_excel(writer, sheet_name="Księga kodów", index=False)
            frequencies_tables = generate_frequencies_table(mapping)
            for frequencies_table in frequencies_tables:
                frequencies_table[0].to_excel(writer, 
                                           startcol=STARTCOL,
                                           startrow=startrow,
                                           sheet_name="Częstości", 
                                           index=False)
                if frequencies_table[1] is not None:
                    frequencies_table[1].to_excel(writer, 
                                            startcol=STARTCOL_PERCENTAGE,
                                            startrow=startrow,
                                            sheet_name="Częstości", 
                                            index=False) 
                startrow += frequencies_table[0].shape[0] + BUFFER 
            if crosstables:
                frequencies_tables = generate_frequencies_table(mapping)
                crosstables_gen = generate_crosstable_merged(mapping, crosstables)
                startrow = 1 
                for frequencies_table in frequencies_tables:
                    startcol = 1
                    frequencies_table[0].drop(columns='% z N').to_excel(writer, 
                                           startcol=STARTCOL,
                                           startrow=startrow,
                                           sheet_name="Krzyżówki", 
                                           index=False)
                    startcol = frequencies_table[0].shape[1]
                    crosstable = next(crosstables_gen)
                    crosstable.to_excel(writer,
                                        startcol=startcol,
                                        startrow=startrow,
                                        sheet_name="Krzyżówki",
                                        index=False)
                    startcol += crosstable.shape[1]
                    startrow += frequencies_table[0].shape[0] + BUFFER
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


def write_crosstable(ws, crosstable: pd.DataFrame, startrow: int, startcol: int) -> int:
    data_col = startcol + 1
    prev_top = None
    merge_start = None
    for i, (top, bot) in enumerate(crosstable.columns):
        col_idx = data_col + i
        if top != prev_top:
            if merge_start is not None:
                if col_idx - 1 > merge_start:
                    ws.merge_cells(
                        start_row=startrow, start_column=merge_start,
                        end_row=startrow, end_column=col_idx - 1
                    )
            ws.cell(row=startrow, column=col_idx, value=top)
            merge_start = col_idx
            prev_top = top
        ws.cell(row=startrow + 1, column=col_idx, value=bot)

    last_col = data_col + len(crosstable.columns) - 1
    if merge_start is not None and last_col > merge_start:
        ws.merge_cells(
            start_row=startrow, start_column=merge_start,
            end_row=startrow, end_column=last_col
        )

    n_index_levels = crosstable.index.nlevels

    for row_i, (idx, row) in enumerate(crosstable.iterrows()):
        current_row = startrow + 2 + row_i
        
        if isinstance(idx, tuple):
            for level_i, level_val in enumerate(idx):
                ws.cell(row=current_row, column=startcol + level_i, value=str(level_val))
        else:
            ws.cell(row=current_row, column=startcol, value=str(idx))
        
        data_col = startcol + n_index_levels
        for col_i, val in enumerate(row):
            ws.cell(row=current_row, column=data_col + col_i, value=val)

    return startrow + 2 + len(crosstable) + BUFFER + CROSSTABLE_BUFFER
