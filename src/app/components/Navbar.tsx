import Link from 'next/link';

function NavLink(props: { name: string; href: string }) {
    return (
        <Link
            key={props.name}
            href={props.href}
            className="flex grow items-center justify-center gap-2 rounded-md text-sm font-large text-white md:flex-none md:justify-start"
        >
            {props.name}
        </Link>
    );
}

export default function Navbar() {
    return (
        <nav className="top-0 w-full sticky flex items-center justify-between px-4 py-4">
            <h1 className="text-white">
                <a href="/">UST SFQ Visualizer</a>
            </h1>
            <div className="flex gap-4">
                <NavLink name="Courses" href="/courses" />
                <NavLink name="Instructors" href="/instructors" />
                <NavLink name="Top" href="#top" />
            </div>
        </nav>
    );
}