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
    excel_to_csv_exc()
