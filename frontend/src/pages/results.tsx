import { useParams } from "react-router-dom";
import { getPortfolio } from "../services/api";
import { useEffect, useState } from "react";
import MatrixTable from "../components/MatrixTable";

export default function Results() {
    const { portfolioId } = useParams<{ portfolioId: string }>();
    const [expandedTicker, setExpandedTicker] = useState<string | null>(null);
    const [portfolio, setPortfolio] = useState<any[]>([]);
    const [portfolioValue, setPortfolioValue] = useState(0);
    const [result, setResult] = useState<any>(null);
    const [username, setUsername] = useState<any>(null);
    let sum = 0;
    useEffect(() => {
        async function queryPortfolio() {
            if (!portfolioId) return;

            try {
                const result = await getPortfolio(portfolioId);

                console.log("Full response:");
                console.log(result);
                setResult(result);
                setUsername(result.username)
                console.log("Portfolio Expanded:");
                setPortfolio(result.portfolioExpanded);
                setPortfolioValue(result.portfolioValue)
            } catch (err) {
                console.error(err);
            }
        }

        queryPortfolio();
    }, [portfolioId]);

    useEffect(() => {
        console.log("Portfolio state updated:");
        console.log(portfolio);

        console.log("Full result:");
        console.log(result);
    }, [portfolio]);




    return (
        <div className="container-fluid">
            <div className="row justify-content-center">
                <div className="col-md-10 text-center">
                    <h1>{username ? `${username}'s Portfolio` : "Portfolio"}</h1>
                    <h3>$
                        {(portfolioValue).toLocaleString(
                            "en-US",
                            {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                            }
                        )}</h3>
                </div>
            </div>
            <hr />
            <div className="row">
                {portfolio.map((stock: any) => (
                    <div className="col-md-3 mt-4" key={stock.ticker} >
                        <div className="card h-100 shadow-sm">
                            <div className="card-body">

                                <div className="text-center">
                                    <img
                                        src={`https://financialmodelingprep.com/image-stock/${stock.ticker}.png`}
                                        alt={stock.ticker}
                                        width={64}
                                    />

                                    <h3>{stock.ticker}</h3>
                                    <h5>{stock.company_name}</h5>

                                    <h4>
                                        $
                                        {(stock.current_price * stock.shares).toLocaleString(
                                            "en-US",
                                            {
                                                minimumFractionDigits: 2,
                                                maximumFractionDigits: 2,
                                            }
                                        )}
                                    </h4>
                                </div>

                                <hr />

                                <button
                                    className="btn btn-outline-primary w-100"
                                    onClick={() =>
                                        setExpandedTicker(
                                            expandedTicker === stock.ticker
                                                ? null
                                                : stock.ticker
                                        )
                                    }
                                >
                                    {expandedTicker === stock.ticker
                                        ? "Hide Details ▲"
                                        : "Show Details ▼"}
                                </button>

                                {expandedTicker === stock.ticker && (
                                    <div className="mt-3">

                                        <p>
                                            <strong>Holding:</strong> {stock.shares}
                                        </p>

                                        <p>
                                            <strong>Cost Basis/Share:</strong> $
                                            {stock.costBasis.toFixed(2)}
                                        </p>

                                        <p>
                                            <strong>Current Price/Share:</strong> $
                                            {stock.current_price.toFixed(2)}
                                        </p>

                                        <p>
                                            <strong>Allocation:</strong>{" "}
                                            {(stock.allocation * 100).toFixed(2)}%
                                        </p>

                                        <p>
                                            <strong>Sector:</strong> {stock.sector}
                                        </p>

                                        <p>
                                            <strong>Industry:</strong> {stock.industry}
                                        </p>

                                        <p>
                                            <strong>P/E:</strong>{" "}
                                            {stock.trailing_pe
                                                ? stock.trailing_pe.toFixed(2)
                                                : "N/A"}
                                        </p>

                                        <p>
                                            <strong>Beta:</strong>{" "}
                                            {stock.beta.toFixed(2)}
                                        </p>

                                    </div>
                                )}

                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="row">
                <div className="col-md-6 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Covariance Matrix</h1>
                            </div>
                            <p className="text-justify">
                                Covariance measures how two assets move relative to one another. A positive covariance indicates they tend to move in the same direction, while a negative covariance indicates they tend to move in opposite directions. Larger positive values suggest a stronger tendency to move together.
                            </p>
                            {result && (
                                <MatrixTable
                                    title="Covariance Matrix"
                                    matrix={result.covarianceMatrix}
                                    decimals={6}
                                />
                            )}
                        </div>
                    </div>
                </div>
                <div className="col-md-6 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Correlation Matrix</h1>
                            </div>
                            <p className="text-justify">
                                Correlation measures how closely two assets move together. A correlation close to +1 indicates they tend to move in the same direction, a correlation close to -1 indicates they tend to move in opposite directions, and a correlation near 0 indicates little relationship between their movements.                            </p>
                            {result && (
                                <MatrixTable
                                    title="Covariance Matrix"
                                    matrix={result.correlationMatrix}
                                    decimals={6}
                                />
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Statisitcal Analysis</h1>
                            </div>
                            <p>There are a few different statistics that were calculated for the
                                portfolio.
                            </p>
                            {result && (
                                <>
                                    <p>Sharpe Ratio: {result.sharpeRatio.toFixed(3)}</p>
                                    <p>HHI: {result.hhi.toFixed(3)}</p>
                                    <p>Annualized Volatility: {(result.portfolioVolatility * 100).toFixed(3)}%</p>
                                    <p>Expected Return: {(result.portfolioReturn * 100).toFixed(3)}%</p>
                                    <p>Portfolio Beta: N/A%</p>
                                </>
                            )}



                        </div>
                    </div>
                </div>
                <div className="col-md-6 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Health Score</h1>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-md-12 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Detailed AI Analysis and Reccomendations</h1>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-md-12 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Fintel "Fin" Bot</h1>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}