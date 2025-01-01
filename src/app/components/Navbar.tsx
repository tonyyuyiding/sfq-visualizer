import Link from 'next/link';

function NavLink(props: { name: string; href: string }) {
    return (
        <Link
            key={props.name}
            href={props.href}
            className="flex grow items-center justify-center gap-2 rounded-md text-normal font-large text-white md:flex-none md:justify-start md:text-base"
        >
            {props.name}
        </Link>
    );
}

export default function Navbar() {
    return (
        <nav className="top-0 w-full sticky flex items-center justify-between px-4 py-4 md:px-8">
            <span className="text-white text-lg">
                <a href="/">UST SFQ Visualizer</a>
            </span>
            <div className="flex gap-4 md:gap-8 md:mr-6">
                <NavLink name="Courses" href="/courses" />
                <NavLink name="Instructors" href="/instructors" />
            </div>
        </nav>
    );
}