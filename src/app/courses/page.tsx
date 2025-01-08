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

export default function CourseRankings() {
    return (
        <div>
            <h1 className="hidden">Course Rankings on SFQ Scores</h1>
            <Ranking items={rankingItems} searchPrompt="Search for courses here..." scoreName="course_mean" />
        </div>
    );
}

export async function generateMetadata({ searchParams }: { searchParams: Promise<{ course_code: string }> }) {
    const courseCode = await searchParams.then(p => p.course_code);
    const isNoIndex = courseCode ? true : false;

    return {
        title: "HKUST Course Rankings on SFQ Scores - HKUST SFQ Visualizer",
        description: "Rankings of courses based on Student Feedback Questionnaire (SFQ) scores",
        keywords: ["HKUST", "SFQ", "Rankings", "Course Review", "Teaching Quality"],
        ...(isNoIndex ? { robots: "noindex" } : {}),
    };
}