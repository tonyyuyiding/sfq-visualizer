"use client";

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

    const colors = [
        "#2565b1", "#e187b2", "#dbb965", "#b5d300", "#a32f33",
        "#007733", "#ee7901", "#9badac", "#78c7a3", "#8b3724",
        "#fed000", "#4096dd", "#00cacd", "#7030a1", "#5c5575",
        "#d9587c", "#e8a784", "#dc7b4a", "#18a079", "#7dc315",
        "#b60081",
    ];

    useEffect(() => {
        const ctx = document.getElementById('line-chart') as HTMLCanvasElement;

        const chartLabels = getSemesterListDSO(datasetsObj);
        const chartDatasets = getDatasetListDSO(datasetsObj, props.mode === "course" ? "itsc" : "course_code", dataKey);

        // const colors = [
        //     "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#E7E9ED", "#76D7C4", "#F7DC6F", "#A569BD", "#5DADE2", "#F1948A"
        // ];

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
                scales: {
                    y: {
                        max: 5,
                        // suggestedMin: 3,
                        ticks: {
                            stepSize: 0.2,
                        },
                        grid: {
                            color: function (context) {
                                if (Number.isInteger(context.tick.value)) {
                                    return '#bbbbbb'
                                } else {
                                    return '#d6d6d6'
                                }
                            },
                            lineWidth: function (context) {
                                if (Number.isInteger(context.tick.value)) {
                                    return 2
                                } else {
                                    return 1
                                }
                            },
                        },
                    },
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuad',
                },
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        align: 'start',
                        title: {
                            display: true,
                            text: 'Legend in alphabet order (Click to hide/show lines)',
                        },
                        labels: {
                            padding: 7,
                            boxHeight: 12,
                            boxWidth: 12,
                        }
                    },
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

        chartRef.current.scales['y'].max = 5;
    }, [dataKey, datasetsObj]);

    return (
        <div className="w-full py-2">
            <div className="p-4 max-w-[90vw] mx-auto flex items-center flex-col gap-4">
                <div className="w-full flex flex-wrap items-center gap-2 justify-between">
                    <h1 className="text-2xl font-bold">{props.title}</h1>
                    <span className="flex gap-2">
                        <ol className="flex items-center gap-1 px-1 border border-gray-500 bg-gray-200 rounded-2xl">
                            <span className={(dataKey === "im" ? "bg-blue-300 " : "") + "rounded-2xl px-2 my-1"}>
                                <input hidden id="radio-instructor-mean" type="radio" name="chart-target" value="instructor-mean" onChange={() => setDataKey("im")} defaultChecked />
                                <label htmlFor="radio-instructor-mean" className={dataKey !== "im" ? "hover:cursor-pointer" : ""}>
                                    Instructor Mean
                                </label>
                            </span>
                            <span className={(dataKey === "cm" ? "bg-blue-300 " : "") + "rounded-2xl px-2 my-1"}>
                                <input hidden id="radio-course-mean" type="radio" name="chart-target" value="course-mean" onChange={() => setDataKey("cm")} />
                                <label htmlFor="radio-course-mean" className={dataKey !== "cm" ? "hover:cursor-pointer" : ""}>
                                    Course Mean
                                </label>
                            </span>
                        </ol>
                    </span>
                </div>
                <div className="w-full h-[70vh] md:h-[75vh] relative border border-gray-500 p-2">
                    <canvas id="line-chart"></canvas>
                </div>
            </div>
        </div>
    );
}