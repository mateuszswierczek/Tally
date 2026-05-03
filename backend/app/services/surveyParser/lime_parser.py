import pandas as pd
from .schema import SurveyQuestion

USED_COLUMNS = ["id", "class", "type/scale", "name", "relevance",
                "text", "language", "validation", "mandator",
                "encrypted", "other"]

class LimeParser:
    def __init__(self, mapping: list[SurveyQuestion]) -> None:
        self.mapping = mapping
        self.df:pd.DataFrame = pd.read_excel("app/services/surveyParser/Test.xlsx", header=None).copy()
        self.last_row = self.df.shape[0]
        self.question_lime_format:list = []
    
    def create_questionnaire(self):
        for index, question in enumerate(self.mapping):
            temp_q_data = {}

            temp_q_data["id"] = f"138{index}"
            match question.question_type:
                case "numerical":
                    temp_q_data["class"] = "Q"
                    temp_q_data["type/scale"] = "T"
                    temp_q_data["name"] = f"G01Q{index}"
                    temp_q_data["relevance"] = 1
                    temp_q_data["text"] = question.text
                    temp_q_data["language"] = "pl"
                    temp_q_data["mandatory"] = "Y"
                    temp_q_data["encrypted"] = "N"
                    temp_q_data["other"] = "N"
                    self.question_lime_format.append(temp_q_data)
                case "single":
                    temp_q_data["class"] = "Q"
                    temp_q_data["type/scale"] = "L"
                    temp_q_data["name"] = f"G01Q{index}"
                    temp_q_data["relevance"] = 1
                    temp_q_data["text"] = question.text
                    temp_q_data["language"] = "pl"
                    temp_q_data["mandatory"] = "Y"
                    temp_q_data["encrypted"] = "N"
                    temp_q_data["other"] = "N"
                    self.question_lime_format.append(temp_q_data)
                    for item in question.cafeteria:
                        temp_q_data = {}
                        temp_q_data["id"] = f"138{index}"
                        temp_q_data["class"] = "A"
                        temp_q_data["type/scale"] = 0
                        temp_q_data["name"] = f"AO{item.index}"
                        #temp_q_data["relevance"] = ""
                        temp_q_data["text"] = item.item
                        temp_q_data["language"] = "pl"
                        #temp_q_data["mandatory"] = ""
                        #temp_q_data["encrypted"] = ""
                        #temp_q_data["other"] = ""
                        self.question_lime_format.append(temp_q_data)
                case "table":
                    pass
                case "text":
                    temp_q_data["class"] = "Q"
                    temp_q_data["type/scale"] = "T"
                    temp_q_data["name"] = f"G01Q{index}"
                    temp_q_data["relevance"] = 1
                    temp_q_data["text"] = question.text
                    temp_q_data["language"] = "pl"
                    temp_q_data["mandatory"] = "Y"
                    temp_q_data["encrypted"] = "N"
                    temp_q_data["other"] = "N"
                    self.question_lime_format.append(temp_q_data)
                case "maq":
                    temp_q_data["class"] = "Q"
                    temp_q_data["type/scale"] = "M"
                    temp_q_data["name"] = f"G01Q{index}"
                    temp_q_data["relevance"] = 1
                    temp_q_data["text"] = question.text
                    temp_q_data["language"] = "pl"
                    temp_q_data["mandatory"] = "Y"
                    temp_q_data["encrypted"] = "N"
                    temp_q_data["other"] = "N"
                    self.question_lime_format.append(temp_q_data)
                    for item in question.cafeteria:
                        temp_q_data = {}
                        temp_q_data["id"] = f"138{index}"
                        temp_q_data["class"] = "SQ"
                        #temp_q_data["type/scale"] = ""
                        temp_q_data["name"] = f"SQ{item.index}"
                        temp_q_data["relevance"] = 1
                        temp_q_data["text"] = item.item
                        temp_q_data["language"] = "pl"
                        #temp_q_data["mandatory"] = ""
                        #temp_q_data["encrypted"] = ""
                        temp_q_data["other"] = "N"
                        self.question_lime_format.append(temp_q_data)
