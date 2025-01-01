import { Metadata } from "next";
import { notFound } from "next/navigation"
import HistoryChart from "../../components/HistoryChart"

type Props = {
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

export default async function Page({ params }: Props) {
    return <CourseChart courseCode={await params.then(p => p.code)} />
}

export const runtime = 'edge';

export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const courseCodeWithSpace = addSpaceToCourseCode(await params.then(p => p.code));

    return {
        title: `${courseCodeWithSpace} SFQ History`,
        description: `SFQ history chart for ${courseCodeWithSpace}`,
        keywords: ["HKUST", "SFQ", "Student Feedback Questionnaire", "Course Review", "Teaching Quality", courseCodeWithSpace],
    };
}