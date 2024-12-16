import os
import pandas as pd

from utils import YSS, YSStqdm, Semester, School


def excel_to_csv(from_path, to_path) -> bool:
    try:
        df = pd.read_excel(from_path)
        os.makedirs(os.path.dirname(to_path), exist_ok=True)
        df.to_csv(to_path, index=False, encoding="utf-8")
        return True
    except FileNotFoundError:
        return False


def excel_to_csv_exc() -> None:
    yss_tqdm = YSStqdm()
    for yss in yss_tqdm:
        yss_tqdm.add(
            excel_to_csv(
                f"raw/{yss.school}/{yss.file_name_xlsx}",
                f"csv_raw/{yss.school}/{yss.file_name_csv}",
            )
        )


def process_csv(directory, yss: YSS) -> pd.DataFrame:
    file_path = os.path.join(directory, yss.file_name_csv)
    
    df = pd.read_csv(file_path)
    
    # Delete unnecessary columns
    df = df.filter(
        items=[
            "Academic Year",
            "Term",
            "Level of Statistics",
            "Course Group",
            "Course No",
            "Section",
            "Instructor's Name",
            "Instructor's ITSC",
            "Enrolment",
            "Response Rate",
            "Course Overall - Mean",
            "Course Overall - SD",
            "Instructor Overall - Mean",
            "Instructor Overall - SD",
        ]
    )
    # Rename columns
    df = df.rename(
        columns={
            "Academic Year": "acad_year",
            "Term": "term",
            "Level of Statistics": "level",
            "Course Group": "course_group",
            "Course No": "course_no",
            "Section": "section",
            "Instructor's Name": "instructor_name",
            "Instructor's ITSC": "instructor_itsc",
            "Enrolment": "num_enrollment",
            "Response Rate": "response_rate",
            "Course Overall - Mean": "course_mean",
            "Course Overall - SD": "course_sd",
            "Instructor Overall - Mean": "instructor_mean",
            "Instructor Overall - SD": "instructor_sd",
        }
    )
    
    # Delete unnessary rows
    df = df.loc[df["acad_year"] == "23-24"]
    df = df.loc[df["level"] == "Instructor"]
    df= df.drop(columns=["level"])
    
    # Delete rows with unexpected values
    df = df.loc[df["num_enrollment"] != "-"]
    
    def to_numeric_with_null(x):
        try:
            return float(x)
        except ValueError:
            return 0
    
    # Type casting
    df["num_enrollment"] = df["num_enrollment"].apply(to_numeric_with_null)
    df["response_rate"] = df["response_rate"].apply(to_numeric_with_null)
    df["course_mean"] = df["course_mean"].apply(to_numeric_with_null)
    df["course_sd"] = df["course_sd"].apply(to_numeric_with_null)
    df["instructor_mean"] = df["instructor_mean"].apply(to_numeric_with_null)
    df["instructor_sd"] = df["instructor_sd"].apply(to_numeric_with_null)
    
    # Calculate the number of responses
    df["num_response"] = round(df["num_enrollment"] * df["response_rate"])
    df.drop(columns=["response_rate"])
    
    return df

if __name__ == "__main__":
    yss = YSS(year=2023, semester=Semester.Fall, school=School.ENG)
    print(process_csv(f"csv_raw/{yss.school}", yss))