import { useState, useEffect } from "react";

interface RankingItemRaw {
    title: string;
    score: number;
    nr: number;
    link: string;
}

interface RankingItemProps {
    rank: number;
    title: string;
    desc: string[];
    link: string;
}


function RankingItem(props: RankingItemProps) {
    return (
        <a href={props.link} className="w-full">
            <div className="px-6 py-4 bg-gray-100 border border-gray-300 rounded-lg hover:shadow-md transition-shadow duration-200">
                <div className="flex gap-4 items-center">
                    <div className="flex flex-shrink-0 flex-grow-0 items-center justify-center w-14 h-14 md:w-12 md:h-12 bg-blue-300 text-gray-800 rounded-full text-lg">
                        {props.rank}
                    </div>
                    <div className="flex-grow-1">
                        <h3 className="text-lg font-bold">{props.title}</h3>
                        <span className="flex flex-wrap gap-x-3">
                            {props.desc.map((d, i) => {
                                return (
                                    <span key={i} className="text-sm">{d}</span>
                                );
                            })}
                        </span>
                    </div>
                </div>
            </div>
        </a>
    );
}

function Ranking(props: { items: RankingItemRaw[], searchPrompt: string, scoreName: string }) {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [filteredItems, setFilteredItems] = useState<RankingItemProps[]>([]);
    const [foundItems, setFoundItems] = useState<RankingItemProps[]>([]);

    useEffect(() => {
        setIsLoading(true);

        let items = props.items;
        // items.sort((a, b) => -(a.score - b.score));

        const minResponses = parseInt(localStorage.getItem('minResponses') || '0', 10);
        items = items.filter((item) => item.nr >= minResponses);
        const numIncluded = items.length;

        let rank = 0;
        let hold = 0;
        let lastScore = Infinity;
        let newFilteredItems: RankingItemProps[] = [];

        for (const item of items) {
            hold++;
            if (item.score < lastScore) {
                lastScore = item.score;
                rank += hold;
                hold = 0;
            }
            newFilteredItems.push({
                rank: rank,
                title: item.title,
                desc: [
                    `${props.scoreName}: ${item.score.toFixed(2)}`,
                    `percentile: ${((1 - (rank - 1) / numIncluded) * 100).toFixed(2)}%`,
                    `num_responses: ${item.nr}`,
                ],
                link: item.link,
            });
        }

        setFilteredItems(newFilteredItems);
    }, [props.items]);

    useEffect(() => {
        setFoundItems(
            filteredItems.filter((item) => {
                return item.title.toLowerCase().includes(searchQuery.toLowerCase());
            })
        );
        setIsLoading(false);
    }, [searchQuery, filteredItems]);

    return (
        <div className="flex flex-col items-center">
            {
                props.searchPrompt && (
                    <div className="w-full max-w-md bg-background">
                        <input type="text" placeholder={props.searchPrompt} className="w-full max-w-md px-4 py-2 mt-6 bg-transparent border-0 border-b border-black focus:outline-none text-lg text-center" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                        <p className="text-sm text-center text-gray-500 mt-2 mb-2">
                            (Click an item to view a more detailed chart of it)
                        </p>
                    </div>
                )
            }
            <div className="flex flex-col items-center gap-4 my-6 px-4">
                {
                    isLoading && <p>Loading...</p>
                }
                {
                    foundItems.map((item, index) => {
                        return (
                            <div key={index} className="w-full max-w-md px-1">
                                <RankingItem {...item} />
                            </div>
                        );
                    })
                }
            </div>
        </div>
    )
}

export {
    type RankingItemRaw,
    Ranking,
}