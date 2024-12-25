"use client";

import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react'

import CourseRankings from './CourseRankings';
import CourseChart from './CourseChart';

function CoursesInner() {
    const searchParams = useSearchParams();
    const course_code = searchParams.get('course_code');

    if (course_code === null) {
        return (
            <CourseRankings />
        );
    }
    else {
        return (
            <CourseChart courseCode={course_code} />
        );
    }
}


export default function Courses() {
    return (
        <Suspense>
            <CoursesInner />
        </Suspense>
    )
}