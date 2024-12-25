import os
import json
import pandas as pd
from tqdm import tqdm


# NOTE: score 0 is a placeholder. The minimum score is 1.


def merge_with_mean(df: pd.DataFrame, col_groupby: str, col_mean: str, col_count: str) -> pd.DataFrame:
    df["_mean_times_response"] = df[col_mean] * df[col_count]
    grouped = df.groupby(col_groupby)
    df = grouped.agg({"_mean_times_response": "sum", col_count: "sum"})
    df[col_mean] = df["_mean_times_response"] / df[col_count]
    df.drop(columns=["_mean_times_response"], inplace=True)
    return df


def add_semester(df: pd.DataFrame) -> pd.DataFrame:
    df["semester"] = df["acad_year"] + " " + df["term"].apply(lambda s: s.lower())
    return df


def add_course_code(df: pd.DataFrame) -> pd.DataFrame:
    df["course_code"] = df["course_group"] + " " + df["course_no"]
    return df


def summarize_on_instructors(file_path, save_path=None) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["mean_times_response_instructor"] = df["instructor_mean"] * df["num_response"]

    # grouping and filtering
    grouped_on_instructor = df.groupby(["instructor_name", "instructor_itsc"])
    df = grouped_on_instructor.agg(
        {"mean_times_response_instructor": "sum", "num_response": "sum"}
    )
    df = df.loc[df["num_response"] > 0]
    df["instructor_mean"] = df["mean_times_response_instructor"] / df["num_response"]
    df.drop(columns=["mean_times_response_instructor"], inplace=True)
    df = df.loc[df["instructor_mean"] >= 1]

    # sorting
    df.sort_values(by=["instructor_mean"], ascending=False, inplace=True)
    df["percentile"] = (
        df["instructor_mean"].rank(ascending=True, method="max", pct=True) * 100
    )

    # add itsc and names
    df["instructor_itsc"] = df.index.get_level_values("instructor_itsc")
    df["instructor_name"] = df.index.get_level_values("instructor_name")
    df.index = df.index.get_level_values("instructor_itsc")

    if save_path is not None:
        df["num_response"] = df["num_response"].astype(int)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_json(save_path, orient="index", index=True, indent=4)
    return df


def summarize_on_courses(file_path, save_path=None) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["mean_times_response_course"] = df["course_mean"] * df["num_response"]
    df = add_course_code(df)

    # grouping and filtering
    grouped_on_course = df.groupby(["course_code"])
    df = grouped_on_course.agg(
        {"mean_times_response_course": "sum", "num_response": "sum"}
    )
    df = df.loc[df["num_response"] > 0]
    df["course_mean"] = df["mean_times_response_course"] / df["num_response"]
    df.drop(columns=["mean_times_response_course"], inplace=True)
    df = df.loc[df["course_mean"] >= 1]

    # sorting
    df.sort_values(by=["course_mean"], ascending=False, inplace=True)
    df["percentile"] = (
        df["course_mean"].rank(ascending=True, method="max", pct=True) * 100
    )

    if save_path is not None:
        df["num_response"] = df["num_response"].astype(int)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_json(save_path, orient="index", index=True, indent=4)
    return df


def chart_data_instructors(file_path, save_path=None) -> dict:
    df = pd.read_csv(file_path)

    df = add_semester(df)
    df = add_course_code(df)
    res = {}

    # 学期内数据合并， 索引为semester

    itscs = df["instructor_itsc"].unique()
    print("Generating chart data for instructors...")
    for itsc in tqdm(itscs):
        df_filtered = df.loc[df["instructor_itsc"] == itsc][
            [
                "section",
                "semester",
                "course_code",
                "course_mean",
                "instructor_mean",
                "num_response",
            ]
        ]
        df_filtered = df_filtered.rename(
            columns={
                "course_mean": "cm",
                "instructor_mean": "im",
                "num_response": "nr",
            }
        )
        courses = df_filtered["course_code"].unique()
        res_itsc = {}
        for course in courses:
            res_itsc_course = {}
            df_course = df_filtered.loc[df_filtered["course_code"] == course]
            semesters = df_course["semester"].unique()
            for semester in semesters:
                df_semester = df_course.loc[df_course["semester"] == semester]
                df_semester = df_semester.drop(
                    columns=["semester", "course_code"]
                )
                df_semester.index = df_semester["section"]
                df_semester = df_semester.drop(columns=["section"])
                try:
                    res_itsc_course[semester] = df_semester.to_dict(orient="index")
                except ValueError:
                    print(df_course)

            res_itsc[course] = res_itsc_course

        res[itsc] = res_itsc

    if save_path is not None:
        print(f"Saving to {save_path}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as file:
            json.dump(res, file, indent=4)
    return res


if __name__ == "__main__":
    df = summarize_on_instructors("data_files/processed/all_processed_data.csv", "data_files/processed/ranking_instructors.json")
    df = summarize_on_courses("data_files/processed/all_processed_data.csv", "data_files/processed/ranking_courses.json")
    res = chart_data_instructors(
        "data_files/processed/all_processed_data.csv",
        "data_files/processed/chart_data_instructors.json",
    )
    pass


# Design:
# a ranking on instructors, demonstrating the instructor score and number of responses for each
# a ranking on courses, demonstrating the course score and number of responses for each
# chart of each course / instructor
# declare the time period
# an option to filter out those with too few responses
