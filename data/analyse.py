import os
import json
import pandas as pd
from tqdm import tqdm


# NOTE: score 0 is a placeholder. The minimum score is 1.


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
    df["instructor_mean"] = (
        df["mean_times_response_instructor"] / df["num_response"]
    ).round(2)
    df.drop(columns=["mean_times_response_instructor"], inplace=True)
    df = df.loc[df["instructor_mean"] >= 1]

    # sorting
    df.sort_values(by=["instructor_mean"], ascending=False, inplace=True)
    df["percentile"] = (
        df["instructor_mean"].rank(ascending=True, method="max", pct=True).round(4)
        * 100
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
    df["course_mean"] = (df["mean_times_response_course"] / df["num_response"]).round(2)
    df.drop(columns=["mean_times_response_course"], inplace=True)
    df = df.loc[df["course_mean"] >= 1]

    # sorting
    df.sort_values(by=["course_mean"], ascending=False, inplace=True)
    df["percentile"] = (
        df["course_mean"].rank(ascending=True, method="max", pct=True).round(4) * 100
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

    itscs = df["instructor_itsc"].unique()
    print("Generating chart data for instructors...")
    for itsc in tqdm(itscs):
        df_filtered = df.loc[df["instructor_itsc"] == itsc][
            [
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
            df_itsc = df_filtered.loc[df_filtered["course_code"] == course]
            semesters = df_itsc["semester"].unique()
            for semester in semesters:
                df_semester: pd.DataFrame = df_itsc.loc[df_itsc["semester"] == semester]
                df_semester = df_semester.drop(columns=["semester", "course_code"])
                df_semester = df_semester.loc[df_semester["nr"] > 0]
                df_semester["cpd"] = df_semester["cm"] * df_semester["nr"]
                df_semester["ipd"] = df_semester["im"] * df_semester["nr"]
                df_semester = df_semester.agg({"cpd": "sum", "ipd": "sum", "nr": "sum"})
                if isinstance(df_semester, pd.Series):
                    df_semester = df_semester.to_frame().T
                df_semester.loc[df_semester["cpd"] == 0, "nr"] = 1
                df_semester["nr"] = df_semester["nr"].astype(int)
                df_semester["cm"] = (df_semester["cpd"] / df_semester["nr"]).round(2)
                df_semester["im"] = (df_semester["ipd"] / df_semester["nr"]).round(2)
                df_semester = df_semester.drop(columns=["cpd", "ipd"])
                res_itsc_course[semester] = df_semester.to_dict(orient="records")[0]

            res_itsc[course] = res_itsc_course

        res[itsc] = res_itsc

    if save_path is not None:
        print(f"Saving to {save_path}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as file:
            json.dump(res, file)
    return res


def chart_data_courses(file_path, save_path=None) -> dict:
    df = pd.read_csv(file_path)

    df = add_semester(df)
    df = add_course_code(df)
    res = {}

    courses = df["course_code"].unique()
    print("Generating chart data for courses...")
    for course in tqdm(courses):
        df_filtered = df.loc[df["course_code"] == course][
            [
                "semester",
                "instructor_itsc",
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
        itscs = df_filtered["instructor_itsc"].unique()
        res_course = {}
        for itsc in itscs:
            res_course_itsc = {}
            df_itsc = df_filtered.loc[df_filtered["instructor_itsc"] == itsc]
            semesters = df_itsc["semester"].unique()
            for semester in semesters:
                df_semester: pd.DataFrame = df_itsc.loc[df_itsc["semester"] == semester]
                df_semester = df_semester.drop(columns=["semester", "instructor_itsc"])
                df_semester = df_semester.loc[df_semester["nr"] > 0]
                df_semester["cpd"] = df_semester["cm"] * df_semester["nr"]
                df_semester["ipd"] = df_semester["im"] * df_semester["nr"]
                df_semester = df_semester.agg({"cpd": "sum", "ipd": "sum", "nr": "sum"})
                if isinstance(df_semester, pd.Series):
                    df_semester = df_semester.to_frame().T
                df_semester.loc[df_semester["cpd"] == 0, "nr"] = 1
                df_semester["nr"] = df_semester["nr"].astype(int)
                df_semester["cm"] = (df_semester["cpd"] / df_semester["nr"]).round(2)
                df_semester["im"] = (df_semester["ipd"] / df_semester["nr"]).round(2)
                df_semester = df_semester.drop(columns=["cpd", "ipd"])
                res_course_itsc[semester] = df_semester.to_dict(orient="records")[0]

            res_course[itsc] = res_course_itsc

        res[course] = res_course

    if save_path is not None:
        print(f"Saving to {save_path}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w") as file:
            json.dump(res, file)
    return res


def delete_nan_recursion(obj) -> any:
    if isinstance(obj, dict):
        return {k: delete_nan_recursion(v) for k, v in obj.items() if k != "NaN"}
    if isinstance(obj, list):
        return [delete_nan_recursion(v) for v in obj]
    return obj


def delete_nan(file_path) -> None:
    content = None
    with open(file_path, "r") as file:
        content = json.load(file)
    content = delete_nan_recursion(content)
    with open(file_path, "w") as file:
        json.dump(content, file)


if __name__ == "__main__":
    # df = summarize_on_instructors(
    #     "data_files/processed/all_processed_data.csv",
    #     "data_files/processed/ranking_instructors.json",
    # )
    # df = summarize_on_courses(
    #     "data_files/processed/all_processed_data.csv",
    #     "data_files/processed/ranking_courses.json",
    # )
    # res = chart_data_instructors(
    #     "data_files/processed/all_processed_data.csv",
    #     "data_files/processed/chart_data_instructors.json",
    # )
    # res = chart_data_courses(
    #     "data_files/processed/all_processed_data.csv",
    #     "data_files/processed/chart_data_courses.json",
    # )
    # delete_nan("data_files/processed/chart_data_instructors.json")
    # delete_nan("data_files/processed/chart_data_courses.json")
    pass


# Design:
# a ranking on instructors, demonstrating the instructor score and number of responses for each
# a ranking on courses, demonstrating the course score and number of responses for each
# chart of each course / instructor
# declare the time period
# an option to filter out those with too few responses
# NOTE: (im == 0 | cm == 0) && nr == 1 means the number is not available
# NOTE: num_response may not be reliable
# NOTE: some NaN itsc is in the json files. should ignore them when making website
