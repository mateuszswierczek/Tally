from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.ns import qn

doc = Document("/Users/mateusz/Desktop/Projekty/Tally/backend/Test.docx")
def main():
    for x in doc.iter_inner_content():
        if isinstance(x, Paragraph):
            if is_numeric_list(x, doc):
                print(x.text)
        elif isinstance(x, Table):
            header_row = [cell.text for cell in x.rows[0].cells]
            first_col = [row.cells[0].text for row in x.rows[1:]]
            print(header_row)
            print(first_col) 

def is_numeric_list(paragraph, doc):
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

main()