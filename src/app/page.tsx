import "./globals.css";

export default function Home() {
  return (
    <div className="container flex justify-center">
      <div className="my-4 mx-4 max-w-lg py-2">
        <h1 className="text-2xl font-bold text-center py-4">HKUST SFQ Visualizer</h1>

        <div className="border-4 border-w border-gray-300 p-4 mb-2">
          <p className="pb-1">
            It is recommended to use a computer to access this website.
          </p>
          <p className="pb-1">
            Quick Start:
            <a href="/courses" className="m-1 underline text-blue-500">Courses</a>
            <a href="/instructors" className="m-1 underline text-blue-500">Instructors</a>
          </p>
        </div>

        <h2 className="text-xl font-bold py-2 mt-2" id="features">Features</h2>
        <p className="pb-1">
          This website is a tool to visualize the Student Feedback Questionnaire (SFQ) survey results of HKUST.
        </p>
        <p className="pb-1">
          Features include:
        </p>
        <ul className="list-disc list-inside ml-6">
          <li>
            Rankings for courses/instructors based on SFQ results
          </li>
          <li>
            History charts of SFQ results for each course/instructor</li>
        </ul>

        <h2 className="text-xl font-bold py-2 mt-2" id="howtouse">How to use</h2>
        <video className="w-full" controls>
          <source src="/tutorial.mp4" type="video/mp4" />
          Your browser does not support the video tag
        </video>
        <h3 className="text-lg font-bold py-1">1. Rankings</h3>
        <p className="pb-1">
          By clicking on the "Courses" or "Instructors" link in the navigation bar, you can view the rankings of courses or instructors based on SFQ results.
        </p>
        <p className="pb-1">
          You can search for any courses or instructors in the search bar on top of the ranking pages.
        </p>
        <p className="pb-1">
          By clicking on the "Settings" button at the bottom left corner, you can set the minimum total number of responses required for the rankings. The courses/instructors with less than the specified number of responses will not be included.
        </p>
        <h3 className="text-lg font-bold py-1">2. SFQ History Charts</h3>
        <p className="pb-1">
          If you click on any course/instructor in the rankings, you can view the history chart of SFQ results for that course/instructor.
        </p>
        <p className="pb-1">
          Hover on (or click, for mobile devices,) any data point to see the exact score and number of responses.
        </p>
        <p className="pb-1">
          You can switch between "Instructor Mean" and "Course Mean" by clicking on the buttons above the chart. These are the two fields in the Student Feedback Questionnaire.
        </p>
        <p className="pb-1">
          To show/hide some lines in the chart, just click on the legend.
        </p>

        <h2 className="text-xl font-bold py-2 mt-2" id="about">About</h2>
        <p className="pb-1">
          SFQ visualizer is an open source project. You can find the source code on <a href="https://github.com/tonyyuyiding/sfq-visualizer" className="underline" target="_blank">github</a>. If you find this website useful, please star the github repository (Thanks!). Contributions and issues are also welcome!
        </p>
        <p className="pb-1">
          The rankings and charts are completely based on the SFQ survey results published by the university. They have nothing to do with the attitude of the developers. The data is up to Summer 2024.
        </p>
        <p className="pb-1">
          The data is for reference only. Small inaccuracy is possible in calculations. Besides, the SFQ results may be biased. As is mentioned on the university website, large classes tend to get lower ratings, and PG classes usually get higher ratings than UG ones.
        </p>
        <p className="pb-1">
          The project is developed with <code>React</code> and <code>Next.js</code>. The fantastic charts are made with <code>Chart.js</code>. Data is from HKUST official website, processed using <code>Python</code> and <code>pandas</code>. The webpage is deployed on <code>Cloudflare Pages</code>.
        </p>
        <p className="pb-1">
          Email: dyy@cyanfeathers.com
        </p>

        <h2 className="text-xl font-bold py-2 mt-2" id="ulinks">Useful Links</h2>
        <ul className="list-disc list-inside ml-6">
          <li><a href="https://ust.space/home" className="m-1 underline text-blue-500" target="_blank">UST Space</a></li>
        </ul>
        <ul className="list-disc list-inside ml-6">
          <li><a href="https://ust-rankings.com/" className="m-1 underline text-blue-500" target="_blank">UST Rankings</a></li>
        </ul>
        <ul className="list-disc list-inside ml-6">
          <li><a href="https://admlu65.ust.hk/" className="m-1 underline text-blue-500" target="_blank">Timetable Planner</a></li>
        </ul>
        <ul className="list-disc list-inside ml-6">
          <li><a href="https://w5.ab.ust.hk/wcq/cgi-bin/" className="m-1 underline text-blue-500" target="_blank">Class Schedule & Quota</a></li>
        </ul>

        <h2 className="text-xl font-bold py-2 mt-2" id="changelog">Changelog</h2>
        <ul className="list-disc list-inside ml-4">
          <li>
            2026-02-25: Add data for Summer and Fall 2025.
          </li>
          <li>
            2025-08-01: Add data for Spring 2025.
          </li>
          <li>
            2025-04-28: Add data for Fall 2024 and Winter 2025.
          </li>
          <li>
            2025-01-03: Fix some wrong data. Add more content to homepage.
          </li>
          <li>
            2025-01-02: Update URLs.
          </li>
          <li>
            2024-12-27: First release.
          </li>
        </ul>
      </div>
    </div>
  );
}
