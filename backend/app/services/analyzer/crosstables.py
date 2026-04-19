import pandas as pd
from typing import Generator
from app.services.recoder.schema import Question
from app.services.recoder.detector import Detector

def generate_crosstable(
    mapping: list[Question], crosstable: list[str]
) -> Generator[pd.DataFrame, None, None]:
    data = pd.read_csv("/Users/mateusz/Desktop/Projekty/Tally/backend/app/server/data.csv")
    for col in mapping:
        if col.question is None:
            continue
        if col.cafeteria is None:
            yield _create_crosstab(data, col.question, crosstable)
        elif col.subquestions is not None:
            if col.is_maq:
                yield _create_maq_crosstab(col.subquestions, data, col, crosstable)
            else:
                for inner_col in col.subquestions:
                    assert inner_col.question is not None
                    yield _create_crosstab(
                        data, inner_col.question, crosstable,
                        cafeteria=col.cafeteria
                    )
        else:
            yield _create_crosstab(
                data, col.question, crosstable,
                cafeteria=col.cafeteria
            )

def _create_crosstab(
    data: pd.DataFrame,
    question_col: str,
    crosstable: list[str],
    cafeteria=None,
) -> pd.DataFrame:
    categories = [cafe.value for cafe in cafeteria] if cafeteria else None
    question_series = (
        pd.Categorical(data[question_col], categories)
        if categories
        else data[question_col]
    )
    sections = []
    for cross_col in crosstable:
        ct = pd.crosstab(question_series, data[cross_col])
        pct = ct.div(ct.sum(axis=0), axis=1) * 100

        interleaved_rows = []
        for idx in ct.index:
            interleaved_rows.append(ct.loc[idx].rename((idx, "n")))
            interleaved_rows.append(pct.loc[idx].rename((idx, "% z kolumny")))

        section = pd.DataFrame(interleaved_rows)
        section.index = pd.MultiIndex.from_tuples(section.index)
        section.columns = pd.MultiIndex.from_product([[cross_col], ct.columns])
        sections.append(section)

    return pd.concat(sections, axis=1)


def _create_maq_crosstab(
    subquestions: list[Question],
    data: pd.DataFrame,
    col: Question,
    crosstable: list[str],
) -> pd.DataFrame:
    detector = Detector()
    assert col.cafeteria_dump
    main_mapping = {cafe["value"]: cafe["index"] for cafe in col.cafeteria_dump}
    subquestions_columns = [subq.question for subq in subquestions]

    sections = []
    for cross_col in crosstable:
        cross_vals = sorted(data[cross_col].dropna().unique())
        col_data: dict[str, list] = {}

        for val in cross_vals:
            mask = data[cross_col] == val
            subset = pd.DataFrame(data.loc[mask, subquestions_columns].copy())
            subset.columns = [detector.get_cafeteria_item(c) for c in subset.columns]
            for column in subset.columns:
                subset[column] = subset[column].map(main_mapping)
            counts = subset.sum()
            pct = (counts / mask.sum() * 100).round(2)

            interleaved = []
            for idx in counts.index:
                interleaved.append(counts[idx])
                interleaved.append(pct[idx])
            col_data[val] = interleaved

        labels = [subq.question for subq in subquestions if subq.question is not None]
        row_index = pd.MultiIndex.from_tuples(
            [(label, t) for label in labels for t in ("n", "% z kolumny")]
        )
        section = pd.DataFrame(col_data, index=row_index)
        section.columns = pd.MultiIndex.from_product([[cross_col], cross_vals])
        sections.append(section)

    return pd.concat(sections, axis=1)