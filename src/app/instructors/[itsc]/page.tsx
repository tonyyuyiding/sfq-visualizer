import HistoryChart from "../../components/HistoryChart"
import { getNameByItsc } from "../../utils"

type Args = {
    params: Promise<{ itsc: string }>;
}

function InstructorChart(props: { itsc: string }) {
    return (
        <HistoryChart primaryKey={props.itsc} mode="instructor" title={`${getNameByItsc(props.itsc)} SFQ History`} />
    )
}

export default async function Page({ params }: Args) {
    return <InstructorChart itsc={await params.then(p => p.itsc)} />
}

export async function generateMetadata({ params }: Args) {
    const instructorName = getNameByItsc(await params.then(p => p.itsc));

    return {
        title: `${instructorName} student feedback history - HKUST SFQ Visualizer`,
        description: `SFQ history chart for ${instructorName}`,
        keywords: [instructorName, "HKUST", "SFQ", "Instructor Evaluation", "Teaching Quality"],
    };
}