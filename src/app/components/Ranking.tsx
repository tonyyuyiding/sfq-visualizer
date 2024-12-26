export interface RankingItemProps {
    rank: number;
    title: string;
    desc: string[];
    link: string;
}

export function RankingItem(props: RankingItemProps) {
    return (
        <a href={props.link} className="w-full">
            <div className="px-6 py-4 bg-gray-100 border border-gray-300 rounded-lg hover:shadow-md transition-shadow duration-200">
                <div className="flex gap-4 items-center">
                    <div className="flex flex-shrink-0 flex-grow-0 items-center justify-center w-14 h-14 md:w-12 md:h-12 bg-blue-300 text-gray-800 rounded-full text-lg">
                        {props.rank}
                    </div>
                    <div className="flex-grow-1">
                        <h3 className="text-lg font-bold">{props.title}</h3>
                        <p className="text-sm">{props.desc.join(", ")}</p>
                    </div>
                </div>
            </div>
        </a>
    );
}

export function Ranking(props: { items: RankingItemProps[], searchPrompt: string }) {
    return (
        <div className="flex flex-col items-center">
            {
                props.searchPrompt && (
                    <div className="fixed w-full max-w-md color-background">
                        <input type="text" placeholder={props.searchPrompt} className="w-full max-w-md px-4 py-2 mt-6 bg-transparent border-0 border-b border-black focus:outline-none text-lg text-center" />
                        <p className="text-sm text-center text-gray-500 mt-2 mb-2">
                            (Click an item to view a more detailed chart)
                        </p>
                    </div>
                )
            }
            <div className="flex flex-col items-center gap-4 my-6 px-4">
                {
                    props.items.map((item, index) => {
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