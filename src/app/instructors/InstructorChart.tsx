import HistoryChart from "../components/HistoryChart"
import { getNameByItsc } from "../utils"

export default function CourseChart(props: { itsc: string }) {
    return (
        <HistoryChart primaryKey={props.itsc} mode="instructor" title={`${getNameByItsc(props.itsc)} SFQ History`} />
    )
}