import os
import pandas as pd


# NOTE: score 0 is a placeholder. The minimum score is 1.


def summarize_on_instructors(file_path, save_path=None) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["mean_times_response_instructor"] = df["instructor_mean"] * df["num_response"]

    # grouping and filtering
    grouped_on_instructor = df.groupby(["instructor_name", "instructor_itsc"])
    df = grouped_on_instructor.agg({"mean_times_response_instructor": "sum", "num_response": "sum"})
    df = df.loc[df["num_response"] > 0]
    df["instructor_mean"] = df["mean_times_response_instructor"] / df["num_response"]
    df.drop(columns=["mean_times_response_instructor"], inplace=True)
    df = df.loc[df["instructor_mean"] >= 1]
    
    # sorting
    df.sort_values(by=["instructor_mean"], ascending=False, inplace=True)
    df["percentile"] = df["instructor_mean"].rank(ascending=True, method="max", pct=True) * 100
    
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
    df["course_code"] = df["course_group"] + " " + df["course_no"]

    # grouping and filtering
    grouped_on_course = df.groupby(["course_code"])
    df = grouped_on_course.agg({"mean_times_response_course": "sum", "num_response": "sum"})
    df = df.loc[df["num_response"] > 0]
    df["course_mean"] = df["mean_times_response_course"] / df["num_response"]
    df.drop(columns=["mean_times_response_course"], inplace=True)
    df = df.loc[df["course_mean"] >= 1]
    
    # sorting
    df.sort_values(by=["course_mean"], ascending=False, inplace=True)
    df["percentile"] = df["course_mean"].rank(ascending=True, method="max", pct=True) * 100

    if save_path is not None:
        df["num_response"] = df["num_response"].astype(int)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_json(save_path, orient="index", index=True, indent=4)
    return df


if __name__ == "__main__":
    df = summarize_on_instructors("data_files/processed/name_itsc_processed_2.csv", "data_files/processed/ranking_instructors.json")
    df = summarize_on_courses("data_files/processed/name_itsc_processed_2.csv", "data_files/processed/ranking_courses.json")
    print(df)


# Design:
# a ranking on instructors, demonstrating the instructor score and number of responses for each
# a ranking on courses, demonstrating the course score and number of responses for each
# chart of each course / instructor
# declare the time period
# an option to filter out those with too few responses