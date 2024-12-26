"use client";

import { useState, useEffect } from "react";

export default function BottomButtons() {
    const [saveMessage, setSaveMessage] = useState<string>("");
    const [showSettings, setShowSettings] = useState(false);
    const [minResponses, setMinResponses] = useState<string>("");

    useEffect(() => {
        const g = localStorage.getItem('minResponses') || '0';
        setMinResponses(parseInt(g, 10).toString());
    }, [showSettings, saveMessage]);

    useEffect(() => {
        setSaveMessage("");
    }, [showSettings]);

    const handleMinResponsesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setMinResponses(e.target.value);
    };

    const handleSaveMinResponses = () => {
        const r = parseInt(minResponses, 10);
        if (Number.isNaN(r)) {
            setSaveMessage("Invalid input");
        }
        else {
            localStorage.setItem('minResponses', minResponses);
            setSaveMessage("Saved, reloading...");
            window.location.reload();
        }
    }

    return (
        <div>
            <div className="fixed bottom-4 left-4 flex flex-col gap-2">
                <button
                    className="bg-blue-500 text-white font-bold py-1 px-2 rounded hover:bg-blue-700"
                    onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                >
                    To Top
                </button>
                <button
                    className="bg-gray-500 text-white font-bold py-1 px-1 rounded hover:bg-gray-700"
                    onClick={() => setShowSettings(true)}
                >
                    Settings
                </button>
            </div>
            {showSettings && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20">
                    <div className="bg-white p-6 rounded-lg shadow-lg mx-4">
                        <h2 className="text-lg font-bold mb-4">Settings</h2>
                        <label className="block mb-2">
                            Min number of responses (for rankings):
                            <input
                                type="text"
                                value={minResponses}
                                onChange={handleMinResponsesChange}
                                className="ml-2 px-2 py-1 border rounded"
                            />
                        </label>
                        <div className="flex gap-2 mt-4 flex-wrap">
                            <button
                                className="bg-ust-yellow text-white font-bold py-1 px-2 rounded"
                                onClick={() => setShowSettings(false)}
                            >
                                Close
                            </button>
                            <button className="bg-blue-500 text-white font-bold py-1 px-2 rounded" onClick={handleSaveMinResponses}>
                                Save and Refresh
                            </button>
                            <span className="px-2 py-1">
                                {saveMessage}
                            </span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}