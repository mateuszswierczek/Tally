import re
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.ns import qn
from schema import SurveyQuestion, SurveyTable, SurveyCafeteria


doc_path = "/Users/mateusz/Desktop/Projekty/Tally/backend/Test.docx"

class QuestionnaireParser:
    def __init__(self, doc) -> None:
        self.doc = Document(doc)
        self.question_dict:dict = self._preparse_doc()
        self.questions_parsed:list = []

    def _preparse_doc(self) -> dict:
        question_dict = {}
        last_seen_question = None
        first_time = False
        for _, ele in enumerate(self.doc.iter_inner_content(), start=1):
            if isinstance(ele, Paragraph):
                if not ele.text.strip():
                    continue
                if self._is_numeric_list(ele, self.doc):
                    question_dict[ele.text] = []
                    last_seen_question = ele.text
                    first_time = True
                else:
                    if first_time:
                        question_dict[last_seen_question].append({"Type":"Normal"})
                        first_time = False
                    question_dict[last_seen_question].append(ele.text)
            elif isinstance(ele, Table):
                header_row = [cell.text for cell in ele.rows[0].cells]
                first_col = [row.cells[0].text for row in ele.rows[1:]]
                question_dict[last_seen_question].append({"Type":"Table"})
                question_dict[last_seen_question].append([header_row, first_col])
        return question_dict
    
    def parser_questionnaire_instrument(self):
        for ind, (key, _) in enumerate(self.question_dict.items(), start=1):
            if self.question_dict[key][0]["Type"] == "Normal":
                question_list = self.question_dict[key][1:]
                question = SurveyQuestion(
                    text=key,
                    index=ind,
                    question_type= "Pojedyńczy wybór",
                    cafeteria=[SurveyCafeteria(item=str(name), index=i) for i, name in enumerate(question_list, start=1)],
                    is_showable=True
                )
            elif self.question_dict[key][0]["Type"] == "Table":
                #TODO: Fajne te list okok
                question_columns = self.question_dict[key][1:][0][0]
                question_rows = self.question_dict[key][1:][0][1]
                question = SurveyTable(
                    text=key,
                    index=ind,
                    question_type="Tabela",
                    cafeteria=[SurveyCafeteria(item=str(name), index=i) for i, name in enumerate(question_rows, start=1)],
                    columns=[SurveyCafeteria(item=str(name), index=i) for i, name in enumerate(question_columns, start=1)],
                    is_showable=True
                )
            else:
                continue
            print(question)
            self.questions_parsed.append(question)
        pass

    @staticmethod
    def _is_numeric_list(paragraph, doc):
        try:
            return bool(int(re.match(r'^\d+\.', paragraph.text.strip()))) #type: ignore
        except (ValueError, TypeError):
            pass
        pPr = paragraph._p.find(qn('w:pPr'))
        if pPr is None:
            return False
        numPr = pPr.find(qn('w:numPr'))
        if numPr is None:
            return False
        
        numId = numPr.find(qn('w:numId')).get(qn('w:val'))
        ilvl = numPr.find(qn('w:ilvl')).get(qn('w:val'))
        
        numbering = doc.part.numbering_part.numbering_definitions._numbering
        for num in numbering.findall(qn('w:num')):
            if num.get(qn('w:numId')) == numId:
                abstractNumId = num.find(qn('w:abstractNumId')).get(qn('w:val'))
                for abstractNum in numbering.findall(qn('w:abstractNum')):
                    if abstractNum.get(qn('w:abstractNumId')) == abstractNumId:
                        for lvl in abstractNum.findall(qn('w:lvl')):
                            if lvl.get(qn('w:ilvl')) == ilvl:
                                numFmt = lvl.find(qn('w:numFmt')).get(qn('w:val'))
                                return numFmt == 'decimal'
        return False

parser = QuestionnaireParser(doc_path)
parser.parser_questionnaire_instrument()