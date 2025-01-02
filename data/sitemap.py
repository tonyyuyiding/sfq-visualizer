import json

targets = {
    "https://sfq.cyanfeathers.com/": None,
    "https://sfq.cyanfeathers.com/courses": None,
    "https://sfq.cyanfeathers.com/instructors": None,
    "https://sfq.cyanfeathers.com/courses/?": "./data_files/processed/ranking_courses.json",
    "https://sfq.cyanfeathers.com/instructors/?": "./data_files/processed/ranking_instructors.json",
}


def generate_sitemap(targets=targets):
    with open("../public/sitemap.txt", "w") as f:
        for t in targets:
            if targets[t] is None:
                f.write(t + "\n")
            else:
                with open(targets[t], "r") as fj:
                    jdata = json.load(fj)
                    for k in jdata:
                        k = k.replace(" ", "")
                        f.write(t.replace("?", k) + "\n")


if __name__ == "__main__":
    generate_sitemap()