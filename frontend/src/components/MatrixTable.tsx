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

    return (
        <div className="card shadow-sm mt-4">
            <div className="card-header">
                <h5 className="mb-0">{title}</h5>
            </div>

            <div className="card-body table-responsive">
                <table className="table table-bordered table-hover text-center align-middle">
                    <thead>
                        <tr>
                            <th></th>
                            {tickers.map(ticker => (
                                <th key={ticker}>{ticker}</th>
                            ))}
                        </tr>
                    </thead>

                    <tbody>
                        {tickers.map(rowTicker => (
                            <tr key={rowTicker}>
                                <th>{rowTicker}</th>

                                {tickers.map(colTicker => (
                                    <td key={colTicker}>
                                        {matrix[rowTicker][colTicker].toFixed(decimals)}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}