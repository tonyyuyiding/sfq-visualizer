"use client";

import { useSearchParams } from 'next/navigation'
import CourseRankings from './CourseRankings';
import CourseChart from './CourseChart';

export default function Courses() {
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
