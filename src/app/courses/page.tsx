import { Suspense } from "react";
import CourseRanking from "./courseRanking";

export default function Page() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <CourseRanking />
        </Suspense>
    )
}

export async function generateMetadata() {
    return {
        title: "HKUST Course Rankings on SFQ Scores - HKUST SFQ Visualizer",
        description: "Rankings of courses based on Student Feedback Questionnaire (SFQ) scores",
        keywords: ["HKUST", "SFQ", "Rankings", "Course Review", "Teaching Quality"]
    };
}