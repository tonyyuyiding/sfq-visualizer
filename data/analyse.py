import os
import pandas as pd


# NOTE: score 0 is a placeholder. The minimum score is 1.


def summarize_on_instructors(file_path, save_path=None) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["mean_times_response_course"] = df["course_mean"] * df["num_response"]
    df["mean_times_response_instructor"] = df["instructor_mean"] * df["num_response"]

    grouped_on_instructor = df.groupby(["instructor_name", "instructor_itsc"])
    df = grouped_on_instructor.agg({"mean_times_response_instructor": "sum", "num_response": "sum"})
    df = df.loc[df["num_response"] > 0]
    df["instructor_mean"] = df["mean_times_response_instructor"] / df["num_response"]
    df.drop(columns=["mean_times_response_instructor"], inplace=True)
    df = df.loc[df["instructor_mean"] >= 1]
    df.sort_values(by=["instructor_mean", "num_response"], ascending=False, inplace=True)
    
    df["instructor_itsc"] = df.index.get_level_values("instructor_itsc")
    df["instructor_name"] = df.index.get_level_values("instructor_name")
    df.index = df.index.get_level_values("instructor_itsc")

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_json(save_path, orient="index", index=True, indent=4)
    return df


if __name__ == "__main__":
    df = summarize_on_instructors("data_files/processed/name_itsc_processed_2.csv", "data_files/processed/ranking_instructors.json")
    print(df)


# Design:
# a ranking on instructors, demonstrating the instructor score and number of responses for each
# a ranking on courses, demonstrating the course score and number of responses for each
# chart of each course / instructor
# declare the time period
