import { notFound } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import { Chart } from "chart.js/auto";

import dataRaw from "../../../data/data_files/processed/chart_data_courses.json";
import { getSemesterListFromObj, getDatasetFromObj, Dataset } from "../utils";
import { runInCleanSnapshot } from "next/dist/server/app-render/clean-async-snapshot-instance";

export default function CourseChart(props: { courseCode: string }) {
    const [dataKey, setDataKey] = useState<"cm" | "im">("im");
    const chartRef = useRef<Chart | null>(null);

    const data = JSON.parse(JSON.stringify(dataRaw));

    const courseCode: string = props.courseCode
    if (courseCode.length < 5) {
        return notFound();
    }

    const courseCodeWithSpace: string = courseCode.slice(0, 4) + " " + courseCode.slice(4);
    if (!(courseCodeWithSpace in data)) {
        return notFound();
    }

    const courseData = data[courseCodeWithSpace];

    useEffect(() => {
        const ctx = document.getElementById('line-chart') as HTMLCanvasElement;

        const chartLabels = getSemesterListFromObj(courseData);
        const chartDatasets = getDatasetFromObj(courseData, "itsc", dataKey);

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
                //         suggestedMax: 5,
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
    }, [dataKey, courseData]);

    return (
        <div className="p-4">
            <p>
                CourseChart for {courseCodeWithSpace} (Click to change lines displayed):
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