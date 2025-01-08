"use client";

import { useSearchParams } from "next/navigation";
import rankingDataRaw from "../../../data/data_files/processed/ranking_courses.json";
import { Ranking, RankingItemRaw } from "../components/Ranking";

const rankingData = JSON.parse(JSON.stringify(rankingDataRaw));
const rankingItems: RankingItemRaw[] = [];

for (const k in rankingData) {
    const v = rankingData[k];
    rankingItems.push({
        title: k,
        score: v.course_mean,
        nr: v.num_response,
        link: "/courses/" + k.slice(0, 4) + k.slice(5),
    });
}

export default function CourseRanking() {
    const searchParams = useSearchParams();
    const course_code = searchParams.get("course_code");
    if (course_code) {
        window.location.href = "/courses/" + course_code;
    }
    else return (
        <div>
            <h1 className="hidden">Course Rankings on SFQ Scores</h1>
            <Ranking items={rankingItems} searchPrompt="Search for courses here..." scoreName="course_mean" />
        </div>
    );
}