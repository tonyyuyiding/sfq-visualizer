import os
import pandas as pd
from datetime import datetime

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
    print("Converting all excel to csv...")
    
    yss_tqdm = YSStqdm()
    for yss in yss_tqdm:
        yss_tqdm.add(
            excel_to_csv(
                f"data_files/raw_excel/{yss.school}/{yss.file_name_xlsx}",
                f"data_files/raw_csv/{yss.school}/{yss.file_name_csv}",
            )
        )


def read_and_process_csv(directory, yss: YSS) -> pd.DataFrame:
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
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
    df = df.loc[df["acad_year"] == yss.academic_year]
    df = df.loc[df["level"] == "Instructor"]
    df = df.drop(columns=["level"])

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
    
    # Convert scores
    if yss < YSS(2020, Semester.Fall, School.ENG):
        df["course_mean"] = df["course_mean"].apply(lambda x: x / 25 + 1)
        df["course_sd"] = df["course_sd"].apply(lambda x: x / 625)
        df["instructor_mean"] = df["instructor_mean"].apply(lambda x: x / 25 + 1)
        df["instructor_sd"] = df["instructor_sd"].apply(lambda x: x / 625)

    return df


def read_process_merge_csv_exc(save_path) -> None:
    print("Processing and Merging all raw csv files... (Note: term summary and breakdown files are skipped)")
    
    log_dir = "logs/merge_log"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    df = None
    yss_tqdm = YSStqdm()
    
    with open(log_file, "w") as log:
        for yss in yss_tqdm:
            if yss.school in (School.TermSummary, School.TermBreakdown):
                log.write(f"SKIPPED: {yss.file_name_csv}\n")
                continue
            try:
                df_new = read_and_process_csv(f"data_files/raw_csv/{yss.school}", yss)
            except FileNotFoundError:
                log.write(f"SKIPPED: {yss.file_name_csv} not found\n")
                continue
            except Exception as e:
                log.write(f"FAILURE: {yss.file_name_csv} with error {e}\n")
                yss_tqdm.add_failure()
                continue
            else:
                if df is None:
                    df = df_new
                else:
                    df = pd.concat([df, df_new], ignore_index=True)
                yss_tqdm.add_success()
                log.write(f"SUCCESS: {yss.file_name_csv}\n")
            
    if df is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False, encoding="utf-8")
    return df


if __name__ == "__main__":
    # excel_to_csv_exc()
    df = read_process_merge_csv_exc(save_path="data_files/processed/all_raw_data.csv")
    print(df)
