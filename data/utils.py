import enum
from tqdm import tqdm
from typing import overload

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


def get_file_name(
    school: School, semester: Semester, year: int, format: str = "xlsx"
) -> str:
    return f"{school}-{semester}{year%100}.{format}"


YEAR_LIST = list(range(2024, 2016, -1))
SEMESTER_LIST = [
    Semester.Winter,
    Semester.Spring,
    Semester.Summer,
    Semester.Fall,
]
SCHOOL_LIST = [
    School.SCI,
    School.ENG,
    School.SBM,
    School.HSS,
    School.CLE,
    School.AIS,
    School.OTHER,
    School.TermSummary,
    School.TermBreakdown,
]


class YSS:

    @staticmethod
    def year_to_academic_year(year: int, semester: Semester) -> str:
        year_two_digit = year % 100
        if semester != Semester.Fall:
            year_two_digit -= 1
        return f"{year_two_digit}-{year_two_digit + 1}"

    @staticmethod
    def academic_year_to_year(academic_year: str, semester: Semester) -> int:
        if len(academic_year) != 5:
            raise TypeError("Academic year should be a string with length 5")
        year = int(academic_year[-2:]) + 2000
        if semester == Semester.Fall:
            year -= 1
        return year

    def __init__(self, year: int | str, semester: Semester, school: School):
        """
        :param year: int with 4 digits or str with length 5
        """
        if isinstance(year, int):
            self.year = year
            self.semester = semester
            self.school = school
            self.academic_year = YSS.year_to_academic_year(year, semester)
        elif isinstance(year, str):
            self.academic_year = year
            self.semester = semester
            self.school = school
            self.year = YSS.academic_year_to_year(year, semester)
        else:
            raise TypeError("year should be either int or str")

    @property
    def file_name_xlsx(self):
        return get_file_name(self.school, self.semester, self.year % 100, "xlsx")

    @property
    def file_name_csv(self):
        return get_file_name(self.school, self.semester, self.year % 100, "csv")


class YSStqdm:
    def __init__(
        self,
        year_list: list[int] = YEAR_LIST,
        semester_list: list[Semester] = SEMESTER_LIST,
        school_list: list[School] = SCHOOL_LIST,
        **kwargs,
    ) -> None:
        self.year_list = year_list
        self.semester_list = semester_list
        self.school_list = school_list
        self.kwargs = kwargs
        self.pbar_year, self.pbar_semester, self.pbar_school = None, None, None

    def __iter__(self):
        self.num_success, self.num_failure, self.num_skipped = 0, 0, 0
        with tqdm(self.year_list, **self.kwargs) as pbar_year:
            self.pbar_year = pbar_year
            for year in pbar_year:
                pbar_year.set_description(f"Yr {year}".ljust(10))
                with tqdm(
                    self.semester_list, leave=False, **self.kwargs
                ) as pbar_semester:
                    self.pbar_semester = pbar_semester
                    for semester in pbar_semester:
                        pbar_semester.set_description(f"Sem {semester}".ljust(10))
                        with tqdm(
                            self.school_list, leave=False, **self.kwargs
                        ) as pbar_school:
                            self.pbar_school = pbar_school
                            for school in pbar_school:
                                pbar_school.set_description(f"Sch {school}".ljust(10))
                                self.num_skipped += 1
                                yield YSS(year, semester, school)
                            self.pbar_school = None
                    self.pbar_semester = None
            self.pbar_year = None
        print(
            f"Success: {self.num_success}, Failure: {self.num_failure}, Skipped: {self.num_skipped}"
        )

    def add_success(self) -> None:
        self.pbar_school.colour = "green"
        self.num_success += 1
        self.num_skipped -= 1

    def add_failure(self) -> None:
        self.pbar_school.colour = "red"
        self.num_failure += 1
        self.num_skipped -= 1

    def add(self, succ: bool) -> bool:
        if succ:
            self.add_success()
        else:
            self.add_failure()
        return succ


if __name__ == "__main__":
    import time

    print("testing YSStqdm")

    yss = YSStqdm()
    for i in yss:
        time.sleep(0.02)

    print("Finished")
