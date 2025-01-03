import HistoryChart from "../../components/HistoryChart"
import { getNameByItsc } from "../../utils"

type Props = {
    params: Promise<{ itsc: string }>;
}

function InstructorChart(props: { itsc: string }) {
    return (
        <HistoryChart primaryKey={props.itsc} mode="instructor" title={`${getNameByItsc(props.itsc)} SFQ History`} />
    )
}

export default async function Page({ params }: Props) {
    return <InstructorChart itsc={await params.then(p => p.itsc)} />
}

export const runtime = 'edge';

export async function generateMetadata({ params }: Props) {
    const instructorName = getNameByItsc(await params.then(p => p.itsc));

    return {
        title: `${instructorName} SFQ History`,
        description: `SFQ history chart for ${instructorName}`,
        keywords: ["HKUST", "SFQ", "Student Feedback Questionnaire", "Instructor Evaluation", "Teaching Quality", instructorName],
    };
}