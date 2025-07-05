import type { Metadata } from "next";
import { Analytics } from '@vercel/analytics/next';
import "./globals.css";
import Navbar from "./components/Navbar";
import BottomButtons from "./components/BottomButtons";

export const metadata: Metadata = {
  title: "HKUST SFQ Visualizer",
  description: "HKUST SFQ Visualizer is a tool to visualize the Student Feedback Questionnaire (SFQ) survey results of HKUST.",
  keywords: ["HKUST", "SFQ", "Course Review", "Student Feedback Questionnaire", "HKUST SFQ Visualizer"],
  icons: "/favicon.ico",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="text-gray-900 pb-16">
        <span id="top"></span>

        <Navbar />

        <div>
          {children}
        </div>

        <BottomButtons />

        <Analytics />
      </body>
    </html>
  );
}