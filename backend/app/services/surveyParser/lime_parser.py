import pandas as pd
from .schema import SurveyQuestion

df = pd.read_excel("app/services/surveyParser/Test.xlsx", header=None)

last_rwo = df.shape[0]


class LimeParser:
    def __init__(self, mapping: list[SurveyQuestion]) -> None:
        self.mapping = mapping
        self.df:pd.DataFrame = pd.read_excel("app/services/surveyParser/Test.xlsx", header=None).copy()

    def create_questionnaire(self):
        for question in self.mapping:
            print(question)
            match question.question_type:
                case "Numeryczna":
                    pass
                case "Pojedyńczy wybór":
                    pass
                case "Tabela":
                    pass
                case "Tekstowa":
                    pass
                case "Wielokrotnego wyboru":
                    pass
