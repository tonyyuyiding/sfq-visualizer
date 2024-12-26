"use client";

import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react'

import InstructorRankings from './InstructorRankings';
import InstructorChart from './InstructorChart';

function InstructorsInner() {
    const searchParams = useSearchParams();
    const itsc = searchParams.get('itsc');

    if (itsc === null) {
        return (
            <InstructorRankings />
        );
    }
    else {
        return (
            <InstructorChart itsc={itsc} />
        );
    }
}


export default function Instructors() {
    return (
        <Suspense>
            <InstructorsInner />
        </Suspense>
    )
}