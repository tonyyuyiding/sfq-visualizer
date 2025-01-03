import json

targets = {
    "https://sfq.cyanfeathers.com/": None,
    "https://sfq.cyanfeathers.com/courses": None,
    "https://sfq.cyanfeathers.com/instructors": None,
    "https://sfq.cyanfeathers.com/courses/?": "./data_files/processed/ranking_courses.json",
    "https://sfq.cyanfeathers.com/instructors/?": "./data_files/processed/ranking_instructors.json",
}


def generate_sitemap(targets=targets):
    urls = []
    for t in targets:
        if targets[t] is None:
            urls.append(t)
        else:
            with open(targets[t], "r") as fj:
                jdata = json.load(fj)
                for k in jdata:
                    k = k.replace(" ", "")
                    urls.append(t.replace("?", k))
    urls = sorted(urls)
    with open("../public/sitemap.txt", "w") as f:
        f.write("\n".join(urls))


if __name__ == "__main__":
    generate_sitemap()