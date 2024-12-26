import type { Metadata } from "next";
import "./globals.css";
import Navbar from "./components/Navbar";

export const metadata: Metadata = {
  title: "SFQ Visualizer",
  description: "HKUST SFQ Visualizer",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="text-gray-900">
      <span id="top"></span>
        <Navbar />
        <div>
          {children}
        </div>
      </body>
    </html>
  );
}