import os
import requests
from datetime import datetime

from utils import BASE_URL_EXCEL, YSStqdm


def fetch_file(file_name, save_path) -> int:
    url = f"{BASE_URL_EXCEL}/{file_name}"
    r = requests.get(url)

    if r.ok:
        file_path = os.path.join(save_path, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file:
            file.write(r.content)

        return 0
    else:
        return r.status_code


def fetch_file_exc() -> None:
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    yss_tqdm = YSStqdm()

    with open(log_file, "w") as log:
        for yss in yss_tqdm:
            file_name = yss.file_name_xlsx
            status = fetch_file(file_name, f"raw/{yss.school}")
            if status == 0:
                yss_tqdm.add_success()
                log.write(f"SUCCESS: {file_name}\n")
            else:
                yss_tqdm.add_failure()
                log.write(f"FAILURE: {file_name} with status code {status}\n")


if __name__ == "__main__":
    fetch_file_exc()
