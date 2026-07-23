import { useParams } from "react-router-dom";
import { getPortfolio } from "../services/api";
import { useEffect, useState } from "react";

export default function Results() {
    const { portfolioId } = useParams<{ portfolioId: string }>();

    const [portfolio, setPortfolio] = useState<any[]>([]);

    useEffect(() => {
        async function queryPortfolio() {
            if (!portfolioId) return;

            try {
                const result = await getPortfolio(portfolioId);

                console.log("Full response:");
                console.log(result);

                console.log("Portfolio Expanded:");
                console.log(result.portfolioExpanded);

                setPortfolio(result.portfolioExpanded);
            } catch (err) {
                console.error(err);
            }
        }

        queryPortfolio();
    }, [portfolioId]);

    useEffect(() => {
        console.log("Portfolio state updated:");
        console.log(portfolio);
    }, [portfolio]);

    return (
        <div className="container-fluid">
            <div className="row justify-content-center">
                {portfolio.map((stock: any) => (
                    <div className="col-md-10 mt-4" key={stock.ticker}>
                        <div className="card">
                            <div className="card-body">
                                <div className="card-title text-center">
                                    <h3>{stock.ticker}</h3>
                                    <h5>{stock.company_name}</h5>
                                    <h4>${stock.current_price}</h4>
                                </div>

                                <hr />

                                <p>
                                    <strong>Holding:</strong> {stock.shares}
                                </p>

                                <p>
                                    <strong>Cost Basis:</strong> ${stock.costBasis}
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
                                    <strong>P/E:</strong> {stock.trailing_pe}
                                </p>

                                <p>
                                    <strong>Beta:</strong> {stock.beta}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}