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
        link: "/instructors?itsc=" + k,
    });
}

export default function InstructorRankings() {
    return (
        <div>
            <Ranking items={rankingItems} searchPrompt="Search for instructor here..." scoreName="instructor_mean" />
        </div>
    );
}