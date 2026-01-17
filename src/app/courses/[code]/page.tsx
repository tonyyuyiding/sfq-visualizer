import { Metadata } from "next";
import { notFound } from "next/navigation"
import HistoryChart from "../../components/HistoryChart"

type Args = {
    params: Promise<{ code: string }>;
}

function addSpaceToCourseCode(courseCode: string) {
    return courseCode.slice(0, 4) + " " + courseCode.slice(4);
}

function CourseChart(props: { courseCode: string }) {
    if (props.courseCode.length < 5) {
        return notFound();
    }

    const courseCodeWithSpace = addSpaceToCourseCode(props.courseCode);

    return (
        <HistoryChart primaryKey={courseCodeWithSpace} mode="course" title={`${courseCodeWithSpace} SFQ History`} />
    )
}

export default async function Page({ params }: Args) {
    return <CourseChart courseCode={await params.then(p => p.code)} />
}

export async function generateMetadata({ params }: Args): Promise<Metadata> {
    const courseCodeWithSpace = addSpaceToCourseCode(await params.then(p => p.code));

    return {
        title: `${courseCodeWithSpace} student feedback history - HKUST SFQ Visualizer`,
        description: `SFQ history chart for ${courseCodeWithSpace}`,
        keywords: [courseCodeWithSpace, "HKUST", "SFQ", "Course Review", "Teaching Quality"],
    };
}