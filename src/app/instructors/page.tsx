import { Suspense } from "react";
import InstructorRanking from "./instructorRanking";

export default function Page() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <InstructorRanking />
        </Suspense>
    )
}

export async function generateMetadata() {
    return {
        title: "HKUST Instructor Rankings on SFQ Scores - HKUST SFQ Visualizer",
        description: "Rankings of instructors based on Student Feedback Questionnaire (SFQ) scores",
        keywords: ["HKUST", "SFQ", "Rankings", "Instructor Evaluation", "Teaching Quality"]
    };
}