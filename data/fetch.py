import os
import requests
from datetime import datetime

from utils import BASE_URL_EXCEL, YSStqdm


def fetch_file(file_name, save_directory, skip_existing=True) -> int:
    file_path = os.path.join(save_directory, file_name)
    
    if skip_existing and os.path.exists(file_path):
        return -1
    
    url = f"{BASE_URL_EXCEL}/{file_name}"
    r = requests.get(url)

    if r.ok:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file:
            file.write(r.content)

        return 0
    else:
        return r.status_code


def fetch_file_exc() -> None:
    print("Fetching raw files...")
    
    log_dir = "logs/fetch_log"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    yss_tqdm = YSStqdm()

    with open(log_file, "w") as log:
        for yss in yss_tqdm:
            file_name = yss.file_name_xlsx
            status = fetch_file(file_name, f"data_files/raw_excel/{yss.school}")
            if status == 0:
                yss_tqdm.add_success()
                log.write(f"SUCCESS: {file_name}\n")
            elif status == -1:
                yss_tqdm.add_skipped()
                log.write(f"SKIPPED: {file_name} already exists\n")
            else:
                yss_tqdm.add_failure()
                log.write(f"FAILURE: {file_name} with status code {status}\n")


if __name__ == "__main__":
    fetch_file_exc()
