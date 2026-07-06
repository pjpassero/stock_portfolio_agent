import { useState } from "react";
import { getTicker } from '../services/api'
import { analyzePortfolio } from "../services/api";
import type { Position } from "../types/Position";


export default function EnterPortfolio() {
    const [portfolio, setPortfolio] = useState<Position[]>([]);
    const [ticker, setTicker] = useState("None");
    const [price, setPrice] = useState("");
    const [shareCount, setShareCount] = useState("");
    const [costBasis, setCostBasis] = useState("");
    const [response, setReponse] = useState("No Analysis Yet!");




    async function addToPortfolio() {
        try {

            const result = await getTicker(ticker);

            setPrice(result.price);
            const newPosition: Position = {
                ticker: ticker.toUpperCase(),
                shares: Number(shareCount),
                costBasis: Number(costBasis),
                currentBasis: Number(result.price)

            }
            setPortfolio([...portfolio, newPosition]);
            console.log(portfolio)

        } catch (err) {

            console.error(err);

        }
        setTicker("");
        setShareCount("");
        setCostBasis("");

    }
    async function AnalyzePortfolio() {

        if (portfolio.length === 0) {
            alert("Please add a postion")
        } else {
            const result = await analyzePortfolio(portfolio);
            console.log(result);
            setReponse(result.response);
        }


    }
    return (
        <div className="container-fluid">
            <div className="row justify-content-center">
                <div className="col-md-10 mt-5">
                    <div className="card">
                        <div className="card-body justify-content-center">
                            <div className="card-title text-center">
                                <h3>Enter Portfolio Information Here</h3>
                                <h4>{ticker}</h4>
                            </div>
                            <hr />
                            <form>
                                <div className="d-flex flex-column form-group justify-content-center">
                                    <input type="text" className="form-control m-1" value={ticker} onChange={(e) => setTicker(e.target.value)} placeholder="Enter Ticker" />
                                    <input
                                        type="number"
                                        className="form-control m-1"
                                        value={shareCount}
                                        onChange={(e) => setShareCount(e.target.value)}
                                        placeholder="Enter Share Amount"
                                    />

                                    <input
                                        type="number"
                                        className="form-control m-1"
                                        value={costBasis}
                                        onChange={(e) => setCostBasis(e.target.value)}
                                        placeholder="Enter Purchase Price"
                                    />
                                    <button type="button" onClick={addToPortfolio} className="btn btn-primary mb-2">Add to Portfolio</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <hr />
            <div className="row justify-content-center m-5">
                <div className="col-md-12 justify-content-center">
                    <div className="card d-flex flex-column justify-content-center">
                        <div className="card-body justify-content-center">
                            <div className="card-title text-center">
                                <h1>My Portfolio</h1>
                            </div>
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th>Stock Ticker</th>
                                        <th>Share Count</th>
                                        <th>Cost Basis</th>
                                        <th>Current Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {portfolio.map((position) => (
                                        <tr key={position.ticker}>
                                            <td>{position.ticker}</td>
                                            <td>{position.shares}</td>
                                            <td>{position.costBasis}</td>
                                            <td>{position.currentBasis}</td>
                                        </tr>
                                    )

                                    )}
                                </tbody>
                            </table>
                            <button type="button" onClick={AnalyzePortfolio} className="btn btn-primary mb-2">Begin Analysis</button>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row justify-content-center m-5">
                <div className="col-md-12 justify-content-center">
                    <div className="card">
                        <div className="card-body justify-content-center text-jusitfy">
                            <div className="card-title text-center">
                                <h1>Analysis</h1>
                            </div>
                            <p>
                                {response}
                            </p>
                        </div>

                    </div>
                </div>
            </div>

        </div >
    );
}