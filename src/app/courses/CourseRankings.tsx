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
        link: "/courses?course_code=" + k.slice(0, 4) + k.slice(5),
    });
}

export default function CourseRankings() {
    return (
        <div>
            <Ranking items={rankingItems} searchPrompt="Search for courses here..." scoreName="course_mean" />
        </div>
    );
}