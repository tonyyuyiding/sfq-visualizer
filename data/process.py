import os
import pandas as pd

from utils import YSStqdm


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


if __name__ == "__main__":
    # Step 1. Convert all Excel files to CSV files
    # excel_to_csv_exc()
    
    df = pd.read_csv("csv_raw/eng/eng-f23.csv")
    
    # Step 2. Delete unnecessary columns
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
            "Response Rate (Adjusted)",
            "Course Overall - Mean",
            "Course Overall - Mean (Adjusted)",
            "Course Overall - SD",
            "Course Overall -  SD (Adjusted)",
            "Instructor Overall - Mean",
            "Instructor Overall - Mean (Adjusted)",
            "Instructor Overall - SD",
            "Instructor Overall - SD (Adjusted)",
        ]
    )
    # Step 3. Rename columns
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
            "Response Rate (Adjusted)": "response_rate_adj",
            "Course Overall - Mean": "course_mean",
            "Course Overall - Mean (Adjusted)": "course_mean_adj",
            "Course Overall - SD": "course_sd",
            "Course Overall -  SD (Adjusted)": "course_sd_adj",
            "Instructor Overall - Mean": "instructor_mean",
            "Instructor Overall - Mean (Adjusted)": "instructor_mean_adj",
            "Instructor Overall - SD": "instructor_sd",
            "Instructor Overall - SD (Adjusted)": "instructor_sd_adj",
        }
    )
    # Step 4. Delete unnessary rows
    df = df.loc[df["acad_year"] == "23-24"]
    df = df.loc[df["level"].isin(["Course", "Section", "Instructor"])]
    # Step 5. Delete rows with unexpected values
    df = df.loc[df["num_enrollment"] != "-"]
    # Step 6. Type casting
    df["num_enrollment"] = df["num_enrollment"].apply(pd.to_numeric, errors="coerce")
    df["response_rate"] = df["response_rate"].apply(pd.to_numeric, errors="coerce")
    df["response_rate_adj"] = df["response_rate_adj"].apply(pd.to_numeric, errors="coerce")
    df["course_mean"] = df["course_mean"].apply(pd.to_numeric, errors="coerce")
    df["course_mean_adj"] = df["course_mean_adj"].apply(pd.to_numeric, errors="coerce")
    df["course_sd"] = df["course_sd"].apply(pd.to_numeric, errors="coerce")
    df["course_sd_adj"] = df["course_sd_adj"].apply(pd.to_numeric, errors="coerce")
    df["instructor_mean"] = df["instructor_mean"].apply(pd.to_numeric, errors="coerce")
    df["instructor_mean_adj"] = df["instructor_mean_adj"].apply(pd.to_numeric, errors="coerce")
    df["instructor_sd"] = df["instructor_sd"].apply(pd.to_numeric, errors="coerce")
    df["instructor_sd_adj"] = df["instructor_sd_adj"].apply(pd.to_numeric, errors="coerce")
    # Step 7. Calculate the number of responses
    df["num_response"] = round(df["num_enrollment"] * df["response_rate"])
    df["num_response_adj"] = round(df["num_enrollment"] * df["response_rate_adj"])
    df.drop(columns=["response_rate", "response_rate_adj"])
    print(df["num_response"])
