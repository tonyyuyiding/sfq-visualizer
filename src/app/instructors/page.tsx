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

export default function InstructorRankings() {
    return (
        <div>
            <h1 className="hidden">Instructor Rankings on SFQ Scores</h1>
            <Ranking items={rankingItems} searchPrompt="Search for instructor here..." scoreName="instructor_mean" />
        </div>
    );
}

export async function generateMetadata({ searchParams }: { searchParams: Promise<{ itsc: string }> }) {
    const itsc = await searchParams.then(p => p.itsc);
    const isNoIndex = itsc ? true : false;

    return {
        title: "HKUST Instructor Rankings on SFQ Scores - HKUST SFQ Visualizer",
        description: "Rankings of instructors based on Student Feedback Questionnaire (SFQ) scores",
        keywords: ["HKUST", "SFQ", "Rankings", "Instructor Evaluation", "Teaching Quality"],
        ...(isNoIndex ? { robots: "noindex" } : {}),
    };
}