type Props = {
    title: string;
    matrix: Record<string, Record<string, number>>;
    decimals?: number;
};

export default function MatrixTable({
    title,
    matrix,
    decimals = 4,
}: Props) {
    const tickers = Object.keys(matrix);

    const values = tickers.flatMap(rowTicker =>
        tickers.map(colTicker =>
            Math.abs(matrix[rowTicker][colTicker])
        )
    );

    const maxValue = Math.max(...values);

    const getCellStyle = (value: number) => {
        if (value === 0) {
            return {
                backgroundColor: "white",
                color: "black",
            };
        }

        const normalized =
            maxValue === 0
                ? 0
                : Math.abs(value) / maxValue;

        const intensity = 0.2 + (normalized * 0.8);

        if (value < 0) {
            return {
                backgroundColor: `rgba(220, 53, 69, ${intensity})`,
                color: intensity > 0.6 ? "white" : "black",
            };
        }

        return {
            backgroundColor: `rgba(25, 135, 84, ${intensity})`,
            color: intensity > 0.6 ? "white" : "black",
        };
    };

    return (
        <div className="card shadow-sm mt-4">
            <div className="card-header">
                <h5 className="mb-0">{title}</h5>
            </div>

            <div className="card-body table-responsive">
                <table className="table table-bordered text-center align-middle">
                    <thead>
                        <tr>
                            <th></th>

                            {tickers.map(ticker => (
                                <th key={ticker}>
                                    {ticker}
                                </th>
                            ))}
                        </tr>
                    </thead>

                    <tbody>
                        {tickers.map(rowTicker => (
                            <tr key={rowTicker}>
                                <th>{rowTicker}</th>

                                {tickers.map(colTicker => {
                                    const value =
                                        matrix[rowTicker][colTicker];

                                    return (
                                        <td
                                            key={colTicker}
                                            style={getCellStyle(value)}
                                        >
                                            {value.toFixed(decimals)}
                                        </td>
                                    );
                                })}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}