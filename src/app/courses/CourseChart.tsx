import { notFound } from "next/navigation"
import HistoryChart from "../components/HistoryChart"

export default function CourseChart(props: { courseCode: string }) {
    if (props.courseCode.length < 5) {
        return notFound();
    }

    const courseCodeWithSpace = props.courseCode.slice(0, 4) + " " + props.courseCode.slice(4);

    return (
        <HistoryChart primaryKey={courseCodeWithSpace} mode="course" title={`History Chart for ${courseCodeWithSpace}`} />
    )
}