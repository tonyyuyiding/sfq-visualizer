import os
import requests
from datetime import datetime
from tqdm import tqdm

from .utils import Semester, School, get_file_name, BASE_URL_EXCEL


def fetch_file(file_name, save_path="raw") -> int:
    url = f"{BASE_URL_EXCEL}/{file_name}"
    r = requests.get(url)

    if r.ok:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, save_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file:
            file.write(r.content)

        return 0
    else:
        return r.status_code


def fetch_data(year_list, semester_list, school_list) -> None:
    success_count = 0
    failure_count = 0
    log_dir = os.path.join(os.path.dirname(__file__), "log")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    with open(log_file, "w") as log:
        with tqdm(year_list) as pbar_year:
            for year in pbar_year:
                pbar_year.set_description(f"Year {year}")
                with tqdm(semester_list, leave=False) as pbar_semester:
                    for semester in pbar_semester:
                        pbar_semester.set_description(f"Semester {semester}")
                        with tqdm(school_list, leave=False) as pbar_school:
                            for school in pbar_school:
                                pbar_school.set_description(f"School {school}")
                                file_name = get_file_name(school, semester, year)
                                status = fetch_file(
                                    file_name, save_path=f"raw/{school}"
                                )
                                if status == 0:
                                    success_count += 1
                                    pbar_school.colour = "green"
                                    log.write(f"SUCCESS: {file_name}\n")
                                else:
                                    failure_count += 1
                                    pbar_school.colour = "red"
                                    log.write(
                                        f"FAILURE: {file_name} with status code {status}\n"
                                    )

    print(f"Number of successful downloads: {success_count}")
    print(f"Number of failed downloads: {failure_count}")


def main():
    fetch_data(
        year_list=list(range(2024, 2014, -1)),
        semester_list=[
            Semester.Winter,
            Semester.Spring,
            Semester.Summer,
            Semester.Fall,
        ],
        school_list=[
            School.SCI,
            School.ENG,
            School.SBM,
            School.HSS,
            School.CLE,
            School.AIS,
            School.OTHER,
            School.TermSummary,
            School.TermBreakdown,
        ],
    )


if __name__ == "__main__":
    main()
