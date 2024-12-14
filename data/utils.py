import enum

BASE_URL_EXCEL = "https://student-survey.hkust.edu.hk/SFQ_Survey_Results/Excel"


class School(enum.Enum):
    SCI = "sci"
    ENG = "eng"
    SBM = "bm"
    HSS = "hss"
    CLE = "lang"
    AIS = "ais"
    OTHER = "other"
    TermSummary = "tr"
    TermBreakdown = "tbdr"

    def __str__(self):
        return self.value


class Semester(enum.Enum):
    Fall = "f"
    Winter = "w"
    Spring = "s"
    Summer = "sum"

    def __str__(self):
        return self.value


def get_file_name(school: School, semester: Semester, year: int) -> str:
    return f"{school}-{semester}{year%100}.xlsx"
