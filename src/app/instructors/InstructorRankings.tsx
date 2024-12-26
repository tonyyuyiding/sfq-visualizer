import rankingDataRaw from "../../../data/data_files/processed/ranking_instructors.json";
import { Ranking, RankingItemProps } from "../components/Ranking";

const minResponses = parseInt(localStorage.getItem('minResponses') || '0', 10);
const rankingData = JSON.parse(JSON.stringify(rankingDataRaw));
const rankingItemProps: RankingItemProps[] = [];
let rank = 0;
let hold = 0;
let lastScore = Infinity;

let numIncluded = 0;
for (const k in rankingData) {
    const v = rankingData[k];
    if (v.num_response >= minResponses) numIncluded++;
}

for (const k in rankingData) {
    const v = rankingData[k];
    if (v.num_response < minResponses) continue;
    hold++;
    if (v.instructor_mean < lastScore) {
        lastScore = v.instructor_mean;
        rank += hold;
        hold = 0;
    }
    rankingItemProps.push({
        rank: rank,
        title: v.instructor_name,
        desc: [
            `instructor mean: ${v.instructor_mean.toFixed(2)}`,
            `percentile: ${((1 - (rank - 1) / numIncluded) * 100).toFixed(2)}%`,
            `responses: ${v.num_response}`,
        ],
        link: "/instructors?itsc=" + k,
    });
}

export default function InstructorRankings() {
    return (
        <div>
            <Ranking items={rankingItemProps} searchPrompt="Search for instructor here..." />
        </div>
    );
}