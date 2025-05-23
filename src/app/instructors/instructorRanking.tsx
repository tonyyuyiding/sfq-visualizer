"use client";

import { useSearchParams } from "next/navigation";
import rankingDataRaw from "../../../data/data_files/processed/ranking_instructors.json";
import { Ranking, RankingItemRaw } from "../components/Ranking";
import { getNameByItsc } from "../utils";

const rankingData = JSON.parse(JSON.stringify(rankingDataRaw));
const rankingItems: RankingItemRaw[] = [];

for (const k in rankingData) {
    const v = rankingData[k];
    rankingItems.push({
        title: getNameByItsc(k),
        score: v.instructor_mean,
        nr: v.num_response,
        link: "/instructors/" + k,
    });
}

export default function InstructorRanking() {
    const searchParams = useSearchParams();
    const itsc = searchParams.get("itsc");
    if (itsc) {
        window.location.href = "/instructors/" + itsc;
    }
    else return (
        <div>
            <h1 className="hidden">Instructor Rankings on SFQ Scores</h1>
            <Ranking items={rankingItems} searchPrompt="Search for instructor here..." scoreName="instructor_mean" />
        </div>
    );
}