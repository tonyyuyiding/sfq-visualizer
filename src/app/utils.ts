import itscMapJson from "../../data/data_files/processed/itsc_map.json";

const itscMap = JSON.parse(JSON.stringify(itscMapJson));

export function getNameByItsc(itsc: string): string {
    return itsc in itscMap ? itscMap[itsc] : "Unknown";
}

interface DataObj {
    [key: string]: {
        [semester: string]: {
            nr: number;
            cm: number;
            im: number;
        };
    };
}

export interface Dataset {
    label: string;
    data: number[];
    nrs: number[];
}


const terms = ["fall", "winter", "spring", "summer"];


function semesterCmp(a: string, b: string): 1 | 0 | -1 {
    // 1 if a > b, 0 if a == b, -1 if a < b
    // larger means later
    if (a.slice(0, 5) > b.slice(0, 5)) {
        return 1;
    }
    else if (a.slice(0, 5) < b.slice(0, 5)) {
        return -1;
    }
    else {
        const diff = terms.indexOf(a.slice(6)) - terms.indexOf(b.slice(6));
        if (diff > 0) return 1;
        else if (diff < 0) return -1;
        else return 0;
    }
}

export function getSemesterListDSO(obj: DataObj): string[] {
    let semesterSet: Set<string> = new Set();
    for (const [_, v] of Object.entries(obj)) {
        for (const k of Object.keys(v)) {
            semesterSet.add(k);
        };
    }
    return Array.from(semesterSet).sort(semesterCmp);
}

export function getDatasetListDSO(obj: DataObj, secondary_key_type: "itsc" | "course_code", data_key: "cm" | "im"): Dataset[] {
    const semesters = getSemesterListDSO(obj);
    let datasets: Dataset[] = [];
    for (const [k, v] of Object.entries(obj)) {
        let nrs: number[] = [];
        let data: number[] = [];
        for (const sem of semesters) {
            const nr = sem in v ? v[sem]["nr"] : NaN;
            const mean = sem in v ? v[sem][data_key] : NaN;
            if (!(mean < 1)) {
                nrs.push(nr);
                data.push(mean);
            }
        }
        datasets.push({
            label: secondary_key_type === "itsc" ? getNameByItsc(k) : k,
            data: data,
            nrs: nrs,
        });
    }
    return datasets;
}