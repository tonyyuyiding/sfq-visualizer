import rankingDataRaw from "../../../data/data_files/processed/ranking_instructors.json";
import { Ranking, RankingItemProps } from "../components/Ranking";

const rankingData = JSON.parse(JSON.stringify(rankingDataRaw));
const rankingItemProps: RankingItemProps[] = [];
let rank = 0;
let hold = 0;
let lastScore = Infinity;

for (const k in rankingData) {
    const v = rankingData[k];
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
            `percentile: ${v.percentile.toFixed(2)}`,
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