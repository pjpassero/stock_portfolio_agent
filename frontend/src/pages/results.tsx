import { useParams } from "react-router-dom";
import { getPortfolio } from "../services/api";
import { SendMessage } from "../services/api";
import { useEffect, useState } from "react";
import MatrixTable from "../components/MatrixTable";
import PortfolioScoreDial from "../components/PortfolioScoreDial";
import SectorPieChart from "../components/SectorMap";
import TickerPieChart from "../components/StockMap";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
export default function Results() {
    const { portfolioId } = useParams<{ portfolioId: string }>();
    const [expandedTicker, setExpandedTicker] = useState<string | null>(null);
    const [portfolio, setPortfolio] = useState<any[]>([]);
    const [portfolioValue, setPortfolioValue] = useState(0);
    const [result, setResult] = useState<any>(null);
    const [username, setUsername] = useState<any>(null);
    const [ai_summary, setSummary] = useState<any>(null);
    //const [model_portfolio, setModel] = useState<any>(null);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {

        async function queryPortfolio() {

            if (!portfolioId) return;
            setLoading(true);

            try {
                const result = await getPortfolio(portfolioId);
                console.log("Full response:");
                console.log(result);
                setResult(result);
                setUsername(result.username);
                setSummary(result.fin_first_response);
                //setModel(result.model_portfolio);
                console.log("Portfolio Expanded:");
                setPortfolio(result.portfolioExpanded);
                setPortfolioValue(result.portfolio_value);
                setMessages(result.messages || []);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);

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


    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!message.trim() || !portfolioId) {
            return;
        }
        const newMessage = message.trim();

        setMessages(prev => [
            ...prev,
            {
                chat_id: `temp-${Date.now()}`,
                role: "user",
                content: newMessage
            }
        ]);

        setMessage("");

        try {
            const data = await SendMessage(message, portfolioId);
            setMessages(prev => [
                ...prev,
                {
                    chat_id: `temp-fin-${Date.now()}`,
                    role: "assistant",
                    content: data
                }
            ]);


        } catch (error) {
            console.log(error);
        }

    }


    return (

        <div className="container-fluid">
            {loading && (
                <div
                    className="modal show d-block"
                    tabIndex={-1}
                    style={{ backgroundColor: "rgba(0, 0, 0, 0.5)" }}
                >
                    <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content rounded-4 border-0 shadow">

                            <div className="modal-header">
                                <h5 className="modal-title fw-bold">
                                    Loading Your Portfolio
                                </h5>
                            </div>

                            <div className="modal-body text-center">
                                <div
                                    className="spinner-border mb-3"
                                    role="status"
                                />

                                <div className="fw-semibold">
                                    Fin is getting everything ready...
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            )}
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
                    <div className="col-md-3 mt-4" key={stock.ticker}>
                        <div className="card shadow-sm">
                            <div className="card-body">

                                <div className="text-center">
                                    <img
                                        src={`https://financialmodelingprep.com/image-stock/${stock.ticker}.png`}
                                        alt={stock.ticker}
                                        width={64}
                                    />

                                    <h3>{stock.ticker}</h3>
                                    <h5>{stock.company_name ?? "N/A"}</h5>

                                    <h4>
                                        $
                                        {(
                                            (stock.current_price ?? 0) *
                                            (stock.shares ?? 0)
                                        ).toLocaleString("en-US", {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2,
                                        })}
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
                                            <strong>Holding:</strong>{" "}
                                            {stock.shares ?? "N/A"}
                                        </p>

                                        <p>
                                            <strong>Cost Basis/Share:</strong>{" "}
                                            {stock.costBasis != null
                                                ? `$${stock.costBasis.toFixed(2)}`
                                                : "N/A"}
                                        </p>

                                        <p>
                                            <strong>Current Price/Share:</strong>{" "}
                                            {stock.current_price != null
                                                ? `$${stock.current_price.toFixed(2)}`
                                                : "N/A"}
                                        </p>

                                        <p>
                                            <strong>Allocation:</strong>{" "}
                                            {stock.allocation != null
                                                ? `${(stock.allocation * 100).toFixed(2)}%`
                                                : "N/A"}
                                        </p>

                                        <p>
                                            <strong>Sector:</strong>{" "}
                                            {stock.sector ?? "N/A"}
                                        </p>

                                        <p>
                                            <strong>Industry:</strong>{" "}
                                            {stock.industry ?? "N/A"}
                                        </p>

                                        <p>
                                            <strong>P/E:</strong>{" "}
                                            {stock.trailing_pe != null
                                                ? stock.trailing_pe.toFixed(2)
                                                : "N/A"}
                                        </p>

                                        <p>
                                            <strong>Beta:</strong>{" "}
                                            {stock.beta != null
                                                ? stock.beta.toFixed(2)
                                                : "N/A"}
                                        </p>

                                    </div>
                                )}

                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="row">
                <div className="col-md-6 mt-4">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">

                            <div className="text-center mb-4">
                                <h1 className="card-title">Statistical Analysis</h1>
                                <p className="text-muted mb-0">
                                    Key statistics calculated from your portfolio's
                                    performance, risk, and concentration.
                                </p>
                            </div>

                            {result && (
                                <div className="row g-3">

                                    <div className="col-6">
                                        <div className="border rounded p-3 text-center h-100">
                                            <div className="text-muted small mb-1">
                                                Sharpe Ratio
                                            </div>
                                            <div className="fs-3 fw-bold">
                                                {result.sharpe_ratio.toFixed(3)}
                                            </div>
                                            <div className="small text-muted">
                                                Risk-adjusted return
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-6">
                                        <div className="border rounded p-3 text-center h-100">
                                            <div className="text-muted small mb-1">
                                                Sortino Ratio
                                            </div>
                                            <div className="fs-3 fw-bold">
                                                {result.sortino_ratio.toFixed(3)}

                                            </div>
                                            <div className="small text-muted">
                                                Downside Risk-adjusted return
                                            </div>
                                        </div>
                                    </div>
                                    <div className="col-6">
                                        <div className="border rounded p-3 text-center h-100">
                                            <div className="text-muted small mb-1">
                                                HHI
                                            </div>
                                            <div className="fs-3 fw-bold">
                                                {result.hhi.toFixed(3)}
                                            </div>
                                            <div className="small text-muted">
                                                Portfolio concentration
                                            </div>
                                        </div>
                                    </div>

                                    <div className="col-6">
                                        <div className="border rounded p-3 text-center h-100">
                                            <div className="text-muted small mb-1">
                                                Annualized Volatility
                                            </div>
                                            <div className="fs-3 fw-bold">
                                                {(result.volatility * 100).toFixed(2)}%
                                            </div>
                                            <div className="small text-muted">
                                                Annualized risk
                                            </div>
                                        </div>
                                    </div>

                                    <div className="col-6">
                                        <div className="border rounded p-3 text-center h-100">
                                            <div className="text-muted small mb-1">
                                                Expected Return
                                            </div>
                                            <div className="fs-3 fw-bold">
                                                {(result.expected_return * 100).toFixed(2)}%
                                            </div>
                                            <div className="small text-muted">
                                                Annualized expected return
                                            </div>
                                        </div>
                                    </div>

                                    <div className="col-6">
                                        <div className="border rounded p-3 text-center h-100">
                                            <div className="text-muted small mb-1">
                                                Beta
                                            </div>
                                            <div className="fs-3 fw-bold">
                                                {(result.portfolio_beta).toFixed(3)}
                                            </div>
                                            <div className="small text-muted">
                                                Portfolio Beta
                                            </div>
                                        </div>
                                    </div>

                                </div>
                            )}

                        </div>
                    </div>
                </div>
                <div className="col-md-6 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body d-flex flex-column align-items-center">

                            <div className="card-title">
                                <h1>Health Score</h1>
                            </div>

                            <div>
                                <p>
                                    Your score is out of 100. The score is a combination of
                                    all the statistics that were given to Fin for analysis. Fin takes
                                    into account things like the HHI (concentration), the portfolio volatility,
                                    the portfolio return, and how each security moves in relation to one
                                    another.
                                </p>
                            </div>

                            <div>
                                {result && (
                                    <PortfolioScoreDial
                                        score={result.portfolio_score}
                                    />
                                )}
                            </div>

                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-12 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Position Risk Contribution</h1>
                            </div>
                            <div>
                                <p>
                                    <strong>Marginal Risk Contribution:</strong>{" "}
                                    The change in portfolio volatility resulting from a marginal change
                                    in the position's weight.
                                </p>

                                <p>
                                    <strong>Component Contribution to Risk:</strong>{" "}
                                    The portion of total portfolio volatility attributable to a single asset.
                                </p>

                                <p>
                                    <strong>Percentage Contribution to Risk:</strong>{" "}
                                    The asset's component contribution expressed as a percentage of
                                    total portfolio volatility.
                                </p>
                            </div>
                            <div className="table-responsive">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th>Ticker</th>
                                            <th>Allocation</th>
                                            <th>Marginal Risk Contribution</th>
                                            <th>Component Contribution to Risk</th>
                                            <th>Percentage Contribution to Risk</th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {portfolio.map((position) => (
                                            <tr key={position.ticker}>
                                                <td>{position.ticker}</td>

                                                <td>
                                                    {(position.allocation * 100).toFixed(2)}%
                                                </td>

                                                <td>
                                                    {(position.MCR * 100).toFixed(2)}%
                                                </td>

                                                <td>
                                                    {(position.CCR * 100).toFixed(2)}%
                                                </td>

                                                <td>
                                                    {(position.PCR * 100).toFixed(2)}%
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row g-4 mt-1">

                <div className="col-md-6">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body text-center">

                            <h2 className="card-title">
                                Portfolio Allocation
                            </h2>

                            <p className="text-muted">
                                How is your portfolio allocated?
                            </p>

                            {result?.portfolioExpanded && (
                                <TickerPieChart
                                    portfolioExpanded={result.portfolioExpanded}
                                />
                            )}

                        </div>
                    </div>
                </div>

                <div className="col-md-6">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body text-center">

                            <h2 className="card-title">
                                Sector Allocation
                            </h2>

                            <p className="text-muted">
                                Which sectors make up the most of your portfolio?
                            </p>

                            {result?.portfolioExpanded && (
                                <SectorPieChart
                                    portfolioExpanded={result.portfolioExpanded}
                                />
                            )}

                        </div>
                    </div>
                </div>

            </div>

            <div className="row">
                <div className="col-lg-12 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Correlation Matrix</h1>
                            </div>
                            <p className="text-justify">
                                Correlation measures how closely two assets move together. A correlation close to +1 indicates they tend to move in the same direction, a correlation close to -1 indicates they tend to move in opposite directions, and a correlation near 0 indicates little relationship between their movements.


                            </p>
                            {result && (
                                <MatrixTable
                                    title="Correlation Matrix"
                                    matrix={result.correlation}
                                    decimals={6}
                                />
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-lg-12 mt-4 text-justify">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title text-center">
                                <h1>Covariance Matrix</h1>
                            </div>
                            <p className="text-justify">
                                Covariance measures how two assets move relative to one another. A positive covariance indicates they tend to move in the same direction, while a negative covariance indicates they tend to move in opposite directions. Larger positive values suggest a stronger tendency to move together.
                                <br /> <br /> When optimizing a portfolio, you want to lower the covariance between
                                assets to the best of your ability. So if you have 5 tech stocks and want to diversify,
                                you should find a sector that has low or negative covariance with tech.
                            </p>
                            {result && (
                                <MatrixTable
                                    title="Covariance Matrix"
                                    matrix={result.covariance}
                                    decimals={6}
                                />
                            )}
                        </div>
                    </div>
                </div>
            </div>



            <div className="row justify-content-center">
                <div className="col-md-12 mt-4 text-center">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title">
                                <h1>Detailed AI Analysis and Recommendations</h1>
                            </div>

                            <div className="portfolio-analysis text-start">
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        h2: ({ children }) => (
                                            <h2 className="fw-bold mt-4 mb-3">
                                                {children}
                                            </h2>
                                        ),

                                        h3: ({ children }) => (
                                            <h4 className="fw-semibold mt-4 mb-2">
                                                {children}
                                            </h4>
                                        ),

                                        p: ({ children }) => (
                                            <p className="lh-lg mb-3">
                                                {children}
                                            </p>
                                        ),

                                        table: ({ children }) => (
                                            <div className="table-responsive my-4">
                                                <table className="table table-hover align-middle">
                                                    {children}
                                                </table>
                                            </div>
                                        ),

                                        thead: ({ children }) => (
                                            <thead className="table-light">
                                                {children}
                                            </thead>
                                        ),

                                        th: ({ children }) => (
                                            <th className="fw-semibold py-3">
                                                {children}
                                            </th>
                                        ),

                                        td: ({ children }) => (
                                            <td className="py-2">
                                                {children}
                                            </td>
                                        ),

                                        ul: ({ children }) => (
                                            <ul className="lh-lg mb-4">
                                                {children}
                                            </ul>
                                        ),

                                        ol: ({ children }) => (
                                            <ol className="lh-lg mb-4">
                                                {children}
                                            </ol>
                                        ),

                                        li: ({ children }) => (
                                            <li className="mb-2">
                                                {children}
                                            </li>
                                        ),

                                        hr: () => (
                                            <hr className="my-4" />
                                        ),

                                        strong: ({ children }) => (
                                            <strong className="fw-bold">
                                                {children}
                                            </strong>
                                        ),
                                    }}
                                >
                                    {ai_summary ? ai_summary : "Portfolio Analysis"}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                <div className="col-md-12 mt-4 text-center">
                    <div className="card shadow-sm">
                        <div className="card-body">

                            <h1>New Proposed Portfolio Score</h1>

                            <p className="text-muted">

                            </p>

                            {result && result.model_portfolio && (
                                <>
                                    <div className="my-4 d-flex justify-content-center">
                                        <PortfolioScoreDial
                                            score={
                                                result.model_portfolio
                                                    .modeled_portfolio_score
                                            }
                                        />
                                    </div>

                                    <h3>Model Portfolio Stats</h3>

                                    <div className="row mt-3">

                                        <div className="col-6 col-md-3">
                                            <div className="border rounded p-3">
                                                <p className="text-muted mb-1">
                                                    Score
                                                </p>
                                                <h4 className="mb-0">
                                                    {result.model_portfolio
                                                        .modeled_portfolio_score
                                                        .toFixed(2)}
                                                </h4>
                                            </div>
                                        </div>

                                        <div className="col-6 col-md-3">
                                            <div className="border rounded p-3">
                                                <p className="text-muted mb-1">
                                                    Expected Return
                                                </p>
                                                <h4 className="mb-0">
                                                    {(
                                                        result.model_portfolio
                                                            .modeled_return * 100
                                                    ).toFixed(2)}%
                                                </h4>
                                            </div>
                                        </div>

                                        <div className="col-6 col-md-3 mt-3 mt-md-0">
                                            <div className="border rounded p-3">
                                                <p className="text-muted mb-1">
                                                    Sharpe Ratio
                                                </p>
                                                <h4 className="mb-0">
                                                    {result.model_portfolio
                                                        .modeled_sharpe_ratio
                                                        .toFixed(2)}
                                                </h4>
                                            </div>
                                        </div>

                                        <div className="col-6 col-md-3 mt-3 mt-md-0">
                                            <div className="border rounded p-3">
                                                <p className="text-muted mb-1">
                                                    HHI
                                                </p>
                                                <h4 className="mb-0">
                                                    {result.model_portfolio
                                                        .modeled_hhi
                                                        .toFixed(3)}
                                                </h4>
                                            </div>
                                        </div>

                                    </div>
                                    <div className="row mt-3">
                                        <h3 className="text-center mt-5">
                                            Proposed Changes
                                        </h3>

                                        <div className="table-responsive mt-3">
                                            <table className="table table-hover text-center">
                                                <thead>
                                                    <tr>
                                                        <th>Ticker</th>
                                                        <th>Current</th>
                                                        <th>Model</th>
                                                        <th>Change</th>
                                                    </tr>
                                                </thead>

                                                <tbody>
                                                    {result.model_portfolio.positions.map(
                                                        (position: any) => {

                                                            const currentPosition =
                                                                portfolio.find(
                                                                    (p: any) =>
                                                                        p.ticker === position.ticker
                                                                );

                                                            const currentAllocation =
                                                                currentPosition?.allocation ?? 0;

                                                            const modelAllocation =
                                                                position.modeled_allocation ??
                                                                position.allocation ??
                                                                0;

                                                            const change =
                                                                modelAllocation -
                                                                currentAllocation;

                                                            return (
                                                                <tr key={position.ticker}>
                                                                    <td>
                                                                        <strong>
                                                                            {position.ticker}
                                                                        </strong>
                                                                    </td>

                                                                    <td>
                                                                        {(currentAllocation * 100).toFixed(2)}%
                                                                    </td>

                                                                    <td>
                                                                        {(modelAllocation * 100).toFixed(2)}%
                                                                    </td>

                                                                    <td>
                                                                        {(change * 100).toFixed(2)}%
                                                                    </td>
                                                                </tr>
                                                            );
                                                        }
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </>
                            )}

                        </div>
                    </div>
                </div>
            </div>

            <div className="row justify-content-center">
                <div className="col-md-12 mt-4">
                    <div className="card h-100 shadow-sm">
                        <div className="card-body">
                            <div className="card-title text-center">
                                <h1>Ask Fin!</h1>
                            </div>
                            <div
                                className="mb-3 border rounded"
                                style={{
                                    height: "450px",
                                    overflowY: "auto"
                                }}
                            >
                                {messages.map((msg: any) => (
                                    <div
                                        key={msg.chat_id}
                                        className={`p-4 border-bottom ${msg.role === "assistant" ? "bg-light" : ""
                                            }`}
                                    >
                                        <div className="fw-bold mb-2">
                                            {msg.role === "assistant" ? "Fin" : "You"}
                                        </div>

                                        <div>
                                            <ReactMarkdown
                                                remarkPlugins={[remarkGfm, remarkMath]}
                                                rehypePlugins={[rehypeKatex]}
                                            >
                                                {msg.content}
                                            </ReactMarkdown>
                                        </div>
                                    </div>
                                ))}
                            </div>


                            <form onSubmit={handleSubmit}>
                                <div className="input-group">
                                    <input
                                        type="text"
                                        className="form-control"
                                        id="fin_box"
                                        value={message}
                                        onChange={(e) => setMessage(e.target.value)}
                                        placeholder="Ask Fin about your portfolio..."
                                    />

                                    <button
                                        type="submit"
                                        className="btn btn-primary px-4"
                                    >
                                        Send
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <footer className="bg-white border-top text-center py-4 mt-5">
                <div className="container">
                    <p className="mb-0">
                        © {new Date().getFullYear()} FinLab Portfolio analytics provided for educational purposes only.
                        FinLab is not a financial advisory tool, and we are not responsible for investment
                        decisions made using this platform. Please consult a financial professional before
                        making investment decisons. AI-generated content may contain inaccuracies.
                    </p>
                </div>
            </footer>
        </div>
    );
}