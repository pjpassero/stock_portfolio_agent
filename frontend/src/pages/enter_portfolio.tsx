import { useState } from "react";
import { getTicker } from '../services/api'
import { analyzePortfolio } from "../services/api";
import type { Position } from "../types/Position";
import { useNavigate } from "react-router-dom";


export default function EnterPortfolio() {
    const [portfolio, setPortfolio] = useState<Position[]>([]);
    const [ticker, setTicker] = useState("None");
    const [price, setPrice] = useState("");
    const [shareCount, setShareCount] = useState("");
    const [costBasis, setCostBasis] = useState("");
    const [response, setReponse] = useState("No Analysis Yet!");
    const [username, setUsername] = useState("");
    const [experience, setExperience] = useState("");
    const navigate = useNavigate();




    async function addToPortfolio() {
        try {
            const result = await getTicker(ticker);

            const currentPrice =
                result.price === "N/A"
                    ? Number(costBasis)
                    : Number(result.price);

            setPrice(currentPrice.toString());

            const newPosition: Position = {
                ticker: ticker.toUpperCase(),
                shares: Number(shareCount),
                costBasis: Number(costBasis),
                currentBasis: currentPrice
            };

            setPortfolio([...portfolio, newPosition]);

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
            const result = await analyzePortfolio(portfolio, username, experience);
            console.log(result);
            setReponse(result.response);
            navigate(`/results/${result.portfolioId}`);
        }

    }
    return (
        <div className="container-fluid">

            <div className="row justify-content-center">
                <div className="col-lg-10 col-xl-11">

                    <div className="card shadow-sm border-0 rounded-4 mb-4">
                        <div className="card-body p-4 p-md-5">

                            <div className="text-center mb-4">
                                <h2 className="fw-bold mb-2">
                                    Build Your Portfolio
                                </h2>

                                <p className="text-muted mb-0">
                                    Enter a position below to add it to your portfolio.
                                </p>
                            </div>

                            <form>
                                <div className="row g-3">

                                    <div className="col-md-4">
                                        <label
                                            htmlFor="ticker"
                                            className="form-label fw-semibold"
                                        >
                                            Ticker
                                        </label>

                                        <input
                                            id="ticker"
                                            type="text"
                                            className="form-control"
                                            value={ticker}
                                            onChange={(e) => setTicker(e.target.value)}
                                            placeholder="e.g. AAPL"
                                        />
                                    </div>

                                    <div className="col-md-4">
                                        <label
                                            htmlFor="shares"
                                            className="form-label fw-semibold"
                                        >
                                            Shares
                                        </label>

                                        <input
                                            id="shares"
                                            type="number"
                                            className="form-control"
                                            value={shareCount}
                                            onChange={(e) => setShareCount(e.target.value)}
                                            placeholder="e.g. 100"
                                        />
                                    </div>

                                    <div className="col-md-4">
                                        <label
                                            htmlFor="costBasis"
                                            className="form-label fw-semibold"
                                        >
                                            Purchase Price
                                        </label>

                                        <input
                                            id="costBasis"
                                            type="number"
                                            className="form-control"
                                            value={costBasis}
                                            onChange={(e) => setCostBasis(e.target.value)}
                                            placeholder="e.g. 150.00"
                                        />
                                    </div>

                                    <div className="col-12">
                                        <div className="d-grid">
                                            <button
                                                type="button"
                                                onClick={addToPortfolio}
                                                className="btn btn-outline-primary"
                                            >
                                                Add Position
                                            </button>
                                        </div>
                                    </div>

                                </div>
                            </form>

                        </div>
                    </div>


                    <div className="card shadow-sm border-0 rounded-4">
                        <div className="card-body p-4 p-md-5">

                            <div className="text-center mb-4">
                                <h1 className="fw-bold mb-2">
                                    My Portfolio
                                </h1>

                                <p className="text-muted mb-0">
                                    Review your positions before beginning the portfolio analysis.
                                </p>
                            </div>


                            <div className="table-responsive mb-4">
                                <table className="table table-hover align-middle">

                                    <thead className="table-light">
                                        <tr>
                                            <th>Ticker</th>
                                            <th>Shares</th>
                                            <th>Cost Basis</th>
                                            <th>Current Price</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {portfolio.map((position) => (
                                            <tr key={position.ticker}>

                                                <td>
                                                    <span className="fw-semibold">
                                                        {position.ticker}
                                                    </span>
                                                </td>

                                                <td>
                                                    {position.shares}
                                                </td>

                                                <td>
                                                    ${Number(position.costBasis).toFixed(2)}
                                                </td>

                                                <td>
                                                    ${Number(position.currentBasis).toFixed(2)}
                                                </td>

                                            </tr>
                                        ))}
                                    </tbody>

                                </table>
                            </div>


                            <hr className="my-4" />


                            <div className="mb-4">
                                <label
                                    htmlFor="username"
                                    className="form-label fw-semibold"
                                >
                                    Your Name
                                </label>

                                <input
                                    type="text"
                                    className="form-control"
                                    id="username"
                                    placeholder="Enter your name"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                />
                            </div>


                            <div className="mb-4">

                                <label className="form-label fw-semibold">
                                    Investing Experience
                                </label>

                                <p className="text-muted small">
                                    Select the level that best describes your investing knowledge. This will
                                    help us curate the best explanations for you.
                                </p>

                                <div className="d-flex flex-column flex-md-row gap-4">

                                    <div className="form-check">
                                        <input
                                            className="form-check-input"
                                            type="radio"
                                            name="experience"
                                            id="beginner"
                                            value="beginner"
                                            checked={experience === "beginner"}
                                            onChange={(e) => setExperience(e.target.value)}
                                        />
                                        <label
                                            className="form-check-label"
                                            htmlFor="beginner"
                                        >
                                            Beginner
                                        </label>
                                    </div>

                                    <div className="form-check">
                                        <input
                                            className="form-check-input"
                                            type="radio"
                                            name="experience"
                                            id="intermediate"
                                            value="intermediate"
                                            checked={experience === "intermediate"}
                                            onChange={(e) => setExperience(e.target.value)}
                                        />
                                        <label
                                            className="form-check-label"
                                            htmlFor="intermediate"
                                        >
                                            Intermediate
                                        </label>
                                    </div>

                                    <div className="form-check">
                                        <input
                                            className="form-check-input"
                                            type="radio"
                                            name="experience"
                                            id="advanced"
                                            value="advanced"
                                            checked={experience === "advanced"}
                                            onChange={(e) => setExperience(e.target.value)}
                                        />
                                        <label
                                            className="form-check-label"
                                            htmlFor="advanced"
                                        >
                                            Advanced
                                        </label>
                                    </div>

                                </div>
                            </div>


                            <div className="d-grid">
                                <button
                                    type="button"
                                    onClick={AnalyzePortfolio}
                                    className="btn btn-primary btn-lg"
                                >
                                    Analyze Portfolio
                                </button>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
}