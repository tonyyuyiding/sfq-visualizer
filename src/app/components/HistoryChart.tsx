import { notFound } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import { Chart } from "chart.js/auto";

import coursesDataRaw from "../../../data/data_files/processed/chart_data_courses.json";
import instructorsDataRaw from "../../../data/data_files/processed/chart_data_instructors.json";
import { getSemesterListDSO, getDatasetListDSO, Dataset } from "../utils";

const coursesData = JSON.parse(JSON.stringify(coursesDataRaw));
const instructorsData = JSON.parse(JSON.stringify(instructorsDataRaw));

export default function HistoryChart(props: { primaryKey: string, mode: "course" | "instructor", title: string }) {
    const primaryKey = props.primaryKey;
    const data = props.mode === "course" ? coursesData : instructorsData;

    const [dataKey, setDataKey] = useState<"cm" | "im">("im");
    const chartRef = useRef<Chart | null>(null);

    if (!(primaryKey in data)) {
        return notFound();
    }

    const datasetsObj = data[primaryKey];

    useEffect(() => {
        const ctx = document.getElementById('line-chart') as HTMLCanvasElement;

        const chartLabels = getSemesterListDSO(datasetsObj);
        const chartDatasets = getDatasetListDSO(datasetsObj, props.mode === "course" ? "itsc" : "course_code", dataKey);

        const colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#E7E9ED", "#76D7C4", "#F7DC6F", "#A569BD", "#5DADE2", "#F1948A"
        ];

        chartDatasets.forEach((dataset: any, index: number) => {
            dataset.borderColor = colors[index % colors.length];
            dataset.backgroundColor = colors[index % colors.length];
            dataset.pointRadius = 5;
            dataset.pointHoverRadius = 8;
            dataset.tension = 0.3;
        });

        if (chartRef.current) {
            chartRef.current.destroy();
        }

        chartRef.current = new Chart(ctx, {
            "type": "line",
            "data": {
                labels: chartLabels,
                datasets: chartDatasets,
            },
            options: {
                spanGaps: true,
                // scales: {
                //     y: {
                //         max: 5,
                //         suggestedMin: 3,
                //     },
                // },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuad',
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const label = context.dataset.label || '';
                                const obj = context.dataset as Dataset;
                                const nr = obj.nrs[context.dataIndex];
                                const value = context.raw;
                                return `${label}: ${value} (${nr} responses)`;
                            }
                        }
                    }
                }
            }
        });
    }, [dataKey, datasetsObj]);

    return (
        <div className="p-4">
            <p>
                {props.title} (Click to change lines displayed):
            </p>
            <button className="bg-blue-500 text-white py-1 px-1 rounded" onClick={() => setDataKey("cm")} disabled={dataKey === "cm"}>Course Mean</button>
            <button className="bg-blue-500 text-white py-1 px-1 rounded" onClick={() => setDataKey("im")} disabled={dataKey === "im"}>Instructor Mean</button>
            <p>
                Data is from SFQ Results on or before 23-24 spring.
            </p>
            <canvas id="line-chart"></canvas>
        </div>
    );
}