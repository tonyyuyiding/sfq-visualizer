import rankingDataRaw from "../../../data/data_files/processed/ranking_courses.json";
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
    if (v.course_mean < lastScore) {
        lastScore = v.course_mean;
        rank += hold;
        hold = 0;
    }
    rankingItemProps.push({
        rank: rank,
        title: k,
        desc: [
            `course mean: ${v.course_mean.toFixed(2)}`,
            `percentile: ${((1 - (rank - 1) / numIncluded) * 100).toFixed(2)}%`,
            `responses: ${v.num_response}`,
        ],
        link: "/courses?course_code=" + k.slice(0, 4) + k.slice(5),
    });
}

export default function CourseRankings() {
    return (
        <div>
            <Ranking items={rankingItemProps} searchPrompt="Search for courses here..." />
        </div>
    );
}