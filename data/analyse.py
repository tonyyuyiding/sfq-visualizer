import pandas as pd


def summarize_on_instructors():
    df = pd.read_csv("data_files/processed/all_raw_data.csv")

    df["mean_times_response_course"] = df["course_mean"] * df["num_response"]
    df["mean_times_response_instructor"] = df["instructor_mean"] * df["num_response"]

    grouped_on_instructor = df.groupby(["instructor_name", "instructor_itsc"])
    df = grouped_on_instructor.agg({"mean_times_response_instructor": "sum", "num_response": "sum"})
    df["instructor_mean"] = df["mean_times_response_instructor"] / df["num_response"]
    df.drop(columns=["mean_times_response_instructor"], inplace=True)
    df.sort_values(by="instructor_mean", ascending=False, inplace=True)
    
    print(df)

    df.to_csv("data_files/processed/summary_on_instructors.csv", index=False)


if __name__ == "__main__":
    summarize_on_instructors()
