import os
import json
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
    # df = pd.concat((df.loc[df["level"] == "Instructor"], df.loc[df["level"] == "Course"], ))
    df = df.loc[df["level"] == "Instructor"]
    df = df.drop(columns=["level"])

    # Delete rows with unexpected values (no need because try-except is used)
    # df = df.loc[df["num_enrollment"] != "-"]

    def to_numeric_with_null(x):
        """
        NOTE: The number 0 in processed data is a placeholder. The minimum score is 1.
        """
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
        df["course_mean"] = df["course_mean"].apply(lambda x: x / 25 + 1 if x >= 1 else 0)
        df["course_sd"] = df["course_sd"].apply(lambda x: x / 625)
        df["instructor_mean"] = df["instructor_mean"].apply(lambda x: x / 25 + 1 if x >= 1 else 0)
        df["instructor_sd"] = df["instructor_sd"].apply(lambda x: x / 625)

    return df


def read_process_merge_csv_exc(save_path=None) -> pd.DataFrame:
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
            
    if df is not None and save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False, encoding="utf-8")
    return df


def process_itsc_name(file_path, save_path=None, itsc_mode=False) -> None:
    df = pd.read_csv(file_path)
    df_name_itsc = df[["instructor_name", "instructor_itsc"]].drop_duplicates()
    df_name_count = df_name_itsc.groupby("instructor_itsc").agg({"instructor_name": "nunique"})
    df_name_count_filtered = df_name_count.loc[df_name_count["instructor_name"] > 1]
    if df_name_count_filtered.empty:
        print("No duplicated names found")
        return df
    
    json_path = "./settings/itsc_name.json"
    
    try:
        with open(json_path, "r") as file:
            name_settings = json.load(file)
    except FileNotFoundError:
        name_settings = {
            "itsc_Nil": {
                "__name__": "__itsc_to_replace_Nil__",
            },
            "duplicated_name_new_name": {
                "__name__": "__new_name__",
            },
            "duplicated_name_new_itsc": {
                "__name__": "__new_itsc__",
            },
        }
    
    for itsc in df_name_count_filtered.index:
        if itsc == "Nil":
            names = df_name_itsc.loc[df_name_itsc["instructor_itsc"] == itsc]["instructor_name"].values
            print(f"Found names with no itsc: {names}")
            for name in names:
                if name in name_settings["itsc_Nil"]:
                    new_itsc = name_settings["itsc_Nil"][name]
                    print(f"Using setting: {name} -> {new_itsc}")
                else:
                    new_itsc = input(f"> Please enter an itsc for {[name]}: ")
                    name_settings["itsc_Nil"][name] = new_itsc
                df.loc[(df["instructor_itsc"] == itsc) & (df["instructor_name"] == name), "instructor_itsc"] = new_itsc
        
        else:
            names = df_name_itsc.loc[df_name_itsc["instructor_itsc"] == itsc]["instructor_name"].values
            print(f"Found duplicated names for itsc {itsc}: {names}")
            if not itsc_mode:
                for name in names:
                    if name in name_settings["duplicated_name_new_name"]:
                        new_name = name_settings["duplicated_name_new_name"][name]
                        print(f"Using setting: {name} -> {new_name}")
                    else:
                        new_name = input(f"> Please enter a name to replace {[name]}: ")
                        name_settings["duplicated_name_new_name"][name] = new_name
                    df.loc[(df["instructor_itsc"] == itsc) & (df["instructor_name"] == name), "instructor_name"] = new_name
            else:
                for name in names:
                    if name in name_settings["duplicated_name_new_itsc"]:
                        new_itsc = name_settings["duplicated_name_new_itsc"][name]
                        print(f"Using setting: {name} -> {new_itsc}")
                    else:
                        new_itsc = input(f"> Please enter an itsc for {[name]}: ")
                        name_settings["duplicated_name_new_itsc"][name] = new_itsc
                    df.loc[(df["instructor_itsc"] == itsc) & (df["instructor_name"] == name), "instructor_itsc"] = new_itsc
                    
    input("Press Enter to continue...")
                    
    with open(json_path, "w") as file:
        json.dump(name_settings, file, indent=4)
    
    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, encoding="utf-8", index=False)
    return df


def delete_duplicated_data(file_path, save_path=None) -> None:
    df = pd.read_csv(file_path)
    for df_name in df.columns:
        if "Unnamed" in df_name:
            df = df.drop(columns=[df_name])
    df = df.drop_duplicates()
    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False, encoding="utf-8")
    return df
    

if __name__ == "__main__":
    # excel_to_csv_exc()
    # df = read_process_merge_csv_exc(save_path="data_files/processed/all_raw_data.csv")
    # df = process_itsc_name("data_files/processed/all_raw_data.csv", "data_files/processed/name_itsc_processed_1.csv")
    # df = process_itsc_name("data_files/processed/name_itsc_processed_1.csv", "data_files/processed/name_itsc_processed_2.csv", itsc_mode=True)
    # df = delete_duplicated_data("data_files/processed/name_itsc_processed_2.csv", "data_files/processed/all_processed_data.csv")
    pass
