import { useParams } from "react-router-dom";

import { getPortfolio, SendMessage } from "../services/api";

import { useEffect, useState, useRef } from "react";

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

    const [model_portfolio, setModel] = useState<any>(null);

    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState<any[]>([]);

    const messagesEndRef = useRef<HTMLDivElement>(null);


    // =========================================================
    // LOAD PORTFOLIO
    // =========================================================

    useEffect(() => {

        async function queryPortfolio() {

            if (!portfolioId) {
                return;
            }

            try {

                const data = await getPortfolio(portfolioId);

                console.log("Full response:");
                console.log(data);

                setResult(data);

                setUsername(data.username);

                setSummary(data.fin_first_response);

                setModel(data.model_portfolio);

                setPortfolio(data.portfolioExpanded || []);

                setPortfolioValue(data.portfolio_value || 0);

                setMessages(data.messages || []);

            } catch (err) {

                console.error(err);

            }
        }

        queryPortfolio();

    }, [portfolioId]);


    // =========================================================
    // AUTO SCROLL CHAT
    // =========================================================

    useEffect(() => {

        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages]);


    // =========================================================
    // SEND MESSAGE TO FIN
    // =========================================================

    const handleSubmit = async (
        e: React.FormEvent<HTMLFormElement>
    ) => {

        e.preventDefault();

        if (!message.trim() || !portfolioId) {
            return;
        }

        const newMessage = message.trim();


        // Immediately show user message
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

            const data = await SendMessage(
                newMessage,
                portfolioId
            );


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
    };


    // =========================================================
    // PAGE
    // =========================================================

    return (

        <div
            style={{
                backgroundColor: "#f8f9fa",
                minHeight: "100vh"
            }}
        >

            <div
                className="container-fluid py-4 px-3 px-md-4"
                style={{
                    maxWidth: "1500px"
                }}
            >


                {/* =====================================================
                    PORTFOLIO HEADER
                ===================================================== */}

                <div className="row align-items-end mb-5">

                    <div className="col-md-7">

                        <div className="text-uppercase text-muted small fw-semibold mb-1">
                            Portfolio Overview
                        </div>

                        <h1 className="fw-bold mb-1">
                            {username
                                ? `${username}'s Portfolio`
                                : "Portfolio"}
                        </h1>

                        <p className="text-muted mb-0">
                            Risk, allocation, performance, and recommendations.
                        </p>

                    </div>


                    <div className="col-md-5 text-md-end mt-3 mt-md-0">

                        <div className="text-muted small">
                            Total Portfolio Value
                        </div>

                        <h2 className="fw-bold mb-1">

                            {portfolioValue.toLocaleString(
                                "en-US",
                                {
                                    style: "currency",
                                    currency: "USD"
                                }
                            )}

                        </h2>


                        {result && (

                            <div className="text-muted small">

                                Portfolio Health:{" "}

                                <strong className="text-body">
                                    {result.portfolio_score?.toFixed(0)}/100
                                </strong>

                            </div>

                        )}

                    </div>

                </div>



                {/* =====================================================
                    HOLDINGS
                ===================================================== */}

                <div className="d-flex justify-content-between align-items-end mb-3">

                    <div>

                        <h2 className="fw-bold mb-1">
                            Holdings
                        </h2>

                        <p className="text-muted mb-0">
                            Positions currently held in this portfolio.
                        </p>

                    </div>


                    <div className="text-muted small">
                        {portfolio.length} positions
                    </div>

                </div>



                <div className="row g-4">

                    {portfolio.map((stock: any) => (

                        <div
                            className="col-sm-6 col-xl-3"
                            key={stock.ticker}
                        >

                            <div className="card border shadow-sm">

                                <div className="card-body p-4">


                                    {/* STOCK HEADER */}

                                    <div className="d-flex align-items-center gap-3 mb-3">

                                        <img
                                            src={`https://financialmodelingprep.com/image-stock/${stock.ticker}.png`}
                                            alt={stock.ticker}
                                            width={42}
                                            height={42}
                                            className="rounded"
                                            style={{
                                                objectFit: "contain"
                                            }}
                                        />


                                        <div className="overflow-hidden">

                                            <h5 className="fw-bold mb-0">
                                                {stock.ticker}
                                            </h5>

                                            <div
                                                className="text-muted small text-truncate"
                                                title={stock.company_name}
                                            >
                                                {stock.company_name ?? "N/A"}
                                            </div>

                                        </div>

                                    </div>



                                    {/* POSITION VALUE */}

                                    <div className="mb-3">

                                        <div className="text-muted small">
                                            Position Value
                                        </div>

                                        <h4 className="fw-bold mb-1">

                                            {(
                                                (stock.current_price ?? 0) *
                                                (stock.shares ?? 0)
                                            ).toLocaleString(
                                                "en-US",
                                                {
                                                    style: "currency",
                                                    currency: "USD"
                                                }
                                            )}

                                        </h4>


                                        <div className="text-muted small">

                                            {stock.allocation != null
                                                ? `${(
                                                    stock.allocation * 100
                                                ).toFixed(2)}% of portfolio`
                                                : "Allocation N/A"}

                                        </div>

                                    </div>


                                    <hr />


                                    {/* DETAILS BUTTON */}

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



                                    {/* DETAILS */}

                                    {expandedTicker === stock.ticker && (

                                        <div className="mt-4">


                                            <div className="d-flex justify-content-between mb-2">

                                                <span className="text-muted">
                                                    Shares
                                                </span>

                                                <span className="fw-semibold">
                                                    {stock.shares ?? "N/A"}
                                                </span>

                                            </div>


                                            <div className="d-flex justify-content-between mb-2">

                                                <span className="text-muted">
                                                    Cost Basis
                                                </span>

                                                <span className="fw-semibold">

                                                    {stock.costBasis != null
                                                        ? `$${stock.costBasis.toFixed(2)}`
                                                        : "N/A"}

                                                </span>

                                            </div>


                                            <div className="d-flex justify-content-between mb-2">

                                                <span className="text-muted">
                                                    Current Price
                                                </span>

                                                <span className="fw-semibold">

                                                    {stock.current_price != null
                                                        ? `$${stock.current_price.toFixed(2)}`
                                                        : "N/A"}

                                                </span>

                                            </div>


                                            <div className="d-flex justify-content-between mb-2">

                                                <span className="text-muted">
                                                    Sector
                                                </span>

                                                <span className="fw-semibold text-end">
                                                    {stock.sector ?? "N/A"}
                                                </span>

                                            </div>


                                            <div className="d-flex justify-content-between mb-2">

                                                <span className="text-muted">
                                                    Industry
                                                </span>

                                                <span
                                                    className="fw-semibold text-end"
                                                    style={{
                                                        maxWidth: "60%"
                                                    }}
                                                >
                                                    {stock.industry ?? "N/A"}
                                                </span>

                                            </div>


                                            <div className="d-flex justify-content-between mb-2">

                                                <span className="text-muted">
                                                    P/E
                                                </span>

                                                <span className="fw-semibold">

                                                    {stock.trailing_pe != null
                                                        ? stock.trailing_pe.toFixed(2)
                                                        : "N/A"}

                                                </span>

                                            </div>


                                            <div className="d-flex justify-content-between">

                                                <span className="text-muted">
                                                    Beta
                                                </span>

                                                <span className="fw-semibold">

                                                    {stock.beta != null
                                                        ? stock.beta.toFixed(2)
                                                        : "N/A"}

                                                </span>

                                            </div>

                                        </div>

                                    )}

                                </div>

                            </div>

                        </div>

                    ))}

                </div>



                {/* =====================================================
                    PORTFOLIO ANALYTICS
                ===================================================== */}

                <div className="mt-5 mb-3">

                    <h2 className="fw-bold mb-1">
                        Portfolio Analytics
                    </h2>

                    <p className="text-muted mb-0">
                        Risk, return, concentration, and market sensitivity.
                    </p>

                </div>



                <div className="row g-4">


                    {/* STATISTICAL ANALYSIS */}

                    <div className="col-lg-8">

                        <div className="card border shadow-sm h-100">

                            <div className="card-body p-4">

                                <div className="mb-4">

                                    <h3 className="fw-bold mb-1">
                                        Statistical Analysis
                                    </h3>

                                    <p className="text-muted mb-0">
                                        Key measurements calculated from your portfolio.
                                    </p>

                                </div>


                                {result && (

                                    <div className="row g-3">


                                        {/* SHARPE */}

                                        <div className="col-md-4 col-6">

                                            <div className="border rounded p-3 h-100">

                                                <div className="text-muted small mb-1">
                                                    Sharpe Ratio
                                                </div>

                                                <div className="fs-4 fw-bold">
                                                    {result.sharpe_ratio?.toFixed(3)}
                                                </div>

                                                <div className="small text-muted">
                                                    Risk-adjusted return
                                                </div>

                                            </div>

                                        </div>



                                        {/* SORTINO */}

                                        <div className="col-md-4 col-6">

                                            <div className="border rounded p-3 h-100">

                                                <div className="text-muted small mb-1">
                                                    Sortino Ratio
                                                </div>

                                                <div className="fs-4 fw-bold">
                                                    {result.sortino_ratio?.toFixed(3)}
                                                </div>

                                                <div className="small text-muted">
                                                    Downside-adjusted return
                                                </div>

                                            </div>

                                        </div>



                                        {/* HHI */}

                                        <div className="col-md-4 col-6">

                                            <div className="border rounded p-3 h-100">

                                                <div className="text-muted small mb-1">
                                                    HHI
                                                </div>

                                                <div className="fs-4 fw-bold">
                                                    {result.hhi?.toFixed(3)}
                                                </div>

                                                <div className="small text-muted">
                                                    Portfolio concentration
                                                </div>

                                            </div>

                                        </div>



                                        {/* VOLATILITY */}

                                        <div className="col-md-4 col-6">

                                            <div className="border rounded p-3 h-100">

                                                <div className="text-muted small mb-1">
                                                    Volatility
                                                </div>

                                                <div className="fs-4 fw-bold">

                                                    {(result.volatility * 100)
                                                        .toFixed(2)}%

                                                </div>

                                                <div className="small text-muted">
                                                    Annualized risk
                                                </div>

                                            </div>

                                        </div>



                                        {/* EXPECTED RETURN */}

                                        <div className="col-md-4 col-6">

                                            <div className="border rounded p-3 h-100">

                                                <div className="text-muted small mb-1">
                                                    Expected Return
                                                </div>

                                                <div className="fs-4 fw-bold">

                                                    {(result.expected_return * 100)
                                                        .toFixed(2)}%

                                                </div>

                                                <div className="small text-muted">
                                                    Annualized return
                                                </div>

                                            </div>

                                        </div>



                                        {/* BETA */}

                                        <div className="col-md-4 col-6">

                                            <div className="border rounded p-3 h-100">

                                                <div className="text-muted small mb-1">
                                                    Beta
                                                </div>

                                                <div className="fs-4 fw-bold">
                                                    {result.portfolio_beta?.toFixed(3)}
                                                </div>

                                                <div className="small text-muted">
                                                    Market sensitivity
                                                </div>

                                            </div>

                                        </div>

                                    </div>

                                )}

                            </div>

                        </div>

                    </div>



                    {/* HEALTH SCORE */}

                    <div className="col-lg-4">

                        <div className="card border shadow-sm h-100">

                            <div className="card-body p-4 text-center d-flex flex-column">

                                <div>

                                    <h3 className="fw-bold mb-1">
                                        Portfolio Health
                                    </h3>

                                    <p className="text-muted mb-0">
                                        Overall balance between risk, return,
                                        concentration, and diversification.
                                    </p>

                                </div>


                                <div className="flex-grow-1 d-flex align-items-center justify-content-center">

                                    {result && (

                                        <PortfolioScoreDial
                                            score={result.portfolio_score}
                                        />

                                    )}

                                </div>


                                <div className="text-muted small mt-3">
                                    Score ranges from 0 to 100 based on
                                    Fin's portfolio risk model.
                                </div>

                            </div>

                        </div>

                    </div>

                </div>



                {/* =====================================================
                    ALLOCATION CHARTS
                ===================================================== */}

                <div className="row g-4 mt-1">


                    {/* PORTFOLIO ALLOCATION */}

                    <div className="col-lg-6">

                        <div className="card border shadow-sm h-100">

                            <div className="card-body p-4">

                                <div className="text-center mb-3">

                                    <h3 className="fw-bold mb-1">
                                        Portfolio Allocation
                                    </h3>

                                    <p className="text-muted small mb-0">
                                        Allocation by holding
                                    </p>

                                </div>


                                {result?.portfolioExpanded && (

                                    <TickerPieChart
                                        portfolioExpanded={
                                            result.portfolioExpanded
                                        }
                                    />

                                )}

                            </div>

                        </div>

                    </div>



                    {/* SECTOR EXPOSURE */}

                    <div className="col-lg-6">

                        <div className="card border shadow-sm h-100">

                            <div className="card-body p-4">

                                <div className="text-center mb-3">

                                    <h3 className="fw-bold mb-1">
                                        Sector Exposure
                                    </h3>

                                    <p className="text-muted small mb-0">
                                        Allocation by sector
                                    </p>

                                </div>


                                {result?.portfolioExpanded && (

                                    <SectorPieChart
                                        portfolioExpanded={
                                            result.portfolioExpanded
                                        }
                                    />

                                )}

                            </div>

                        </div>

                    </div>

                </div>



                {/* =====================================================
                    MARKET INTELLIGENCE
                ===================================================== */}

                <div className="mt-5 mb-3">

                    <h2 className="fw-bold mb-1">
                        Market Intelligence
                    </h2>

                    <p className="text-muted mb-0">
                        News and events relevant to your holdings.
                    </p>

                </div>


                <div className="card border shadow-sm">

                    <div className="card-body p-4">

                        <div className="d-flex justify-content-between align-items-center">

                            <div>

                                <h3 className="fw-bold mb-1">
                                    Portfolio Headlines
                                </h3>

                                <p className="text-muted mb-0">
                                    Relevant market news will appear here.
                                </p>

                            </div>


                            <span className="badge rounded-pill text-bg-light border">
                                Coming Soon
                            </span>

                        </div>

                    </div>

                </div>



                {/* =====================================================
                    FIN ANALYSIS
                ===================================================== */}

                <div className="mt-5 mb-3">

                    <h2 className="fw-bold mb-1">
                        Fin Analysis
                    </h2>

                    <p className="text-muted mb-0">
                        AI-assisted interpretation of your portfolio.
                    </p>

                </div>


                <div className="card border shadow-sm">

                    <div className="card-body p-4 p-md-5">


                        {/* FIN HEADER */}

                        <div className="d-flex align-items-center gap-3 mb-4">

                            <div
                                className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold"
                                style={{
                                    width: "44px",
                                    height: "44px",
                                    minWidth: "44px"
                                }}
                            >
                                F
                            </div>


                            <div>

                                <h3 className="fw-bold mb-0">
                                    Portfolio Analysis
                                </h3>

                                <small className="text-muted">
                                    Generated by Fin
                                </small>

                            </div>

                        </div>



                        {/* MARKDOWN */}

                        <div className="portfolio-analysis text-start">

                            <ReactMarkdown

                                remarkPlugins={[
                                    remarkGfm
                                ]}

                                components={{

                                    h2: ({ children }) => (

                                        <h3 className="fw-bold mt-4 mb-3">
                                            {children}
                                        </h3>

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

                                    )

                                }}
                            >

                                {ai_summary ??
                                    "Portfolio analysis is loading..."}

                            </ReactMarkdown>

                        </div>

                    </div>

                </div>



                {/* =====================================================
                    MODEL PORTFOLIO
                ===================================================== */}

                <div className="mt-5 mb-3">

                    <h2 className="fw-bold mb-1">
                        Model Portfolio
                    </h2>

                    <p className="text-muted mb-0">
                        Compare your current portfolio with Fin's proposed allocation.
                    </p>

                </div>


                {result?.model_portfolio && (

                    <div className="card border shadow-sm">

                        <div className="card-body p-4 p-md-5">


                            {/* MODEL OVERVIEW */}

                            <div className="row align-items-center g-4 mb-4">


                                {/* MODEL SCORE */}

                                <div className="col-lg-5 text-center">

                                    <h4 className="fw-bold mb-3">
                                        Modeled Health Score
                                    </h4>


                                    <PortfolioScoreDial
                                        score={
                                            result.model_portfolio
                                                .modeled_portfolio_score
                                        }
                                    />

                                </div>



                                {/* MODEL STATS */}

                                <div className="col-lg-7">

                                    <h4 className="fw-bold mb-3">
                                        Current vs. Model
                                    </h4>


                                    <div className="table-responsive">

                                        <table className="table align-middle">

                                            <thead className="table-light">

                                                <tr>
                                                    <th>Metric</th>
                                                    <th>Current</th>
                                                    <th>Model</th>
                                                </tr>

                                            </thead>


                                            <tbody>


                                                {/* SCORE */}

                                                <tr>

                                                    <td className="fw-semibold">
                                                        Score
                                                    </td>

                                                    <td>
                                                        {result.portfolio_score
                                                            .toFixed(2)}
                                                    </td>

                                                    <td className="fw-semibold">

                                                        {result.model_portfolio
                                                            .modeled_portfolio_score
                                                            .toFixed(2)}

                                                    </td>

                                                </tr>



                                                {/* RETURN */}

                                                <tr>

                                                    <td className="fw-semibold">
                                                        Expected Return
                                                    </td>

                                                    <td>

                                                        {(result.expected_return * 100)
                                                            .toFixed(2)}%

                                                    </td>

                                                    <td className="fw-semibold">

                                                        {(result.model_portfolio
                                                            .modeled_return * 100)
                                                            .toFixed(2)}%

                                                    </td>

                                                </tr>



                                                {/* SHARPE */}

                                                <tr>

                                                    <td className="fw-semibold">
                                                        Sharpe Ratio
                                                    </td>

                                                    <td>
                                                        {result.sharpe_ratio
                                                            .toFixed(2)}
                                                    </td>

                                                    <td className="fw-semibold">

                                                        {result.model_portfolio
                                                            .modeled_sharpe_ratio
                                                            .toFixed(2)}

                                                    </td>

                                                </tr>



                                                {/* HHI */}

                                                <tr>

                                                    <td className="fw-semibold">
                                                        HHI
                                                    </td>

                                                    <td>
                                                        {result.hhi.toFixed(3)}
                                                    </td>

                                                    <td className="fw-semibold">

                                                        {result.model_portfolio
                                                            .modeled_hhi
                                                            .toFixed(3)}

                                                    </td>

                                                </tr>

                                            </tbody>

                                        </table>

                                    </div>

                                </div>

                            </div>



                            <hr className="my-4" />



                            {/* REASONING */}

                            <div className="mb-4">

                                <h4 className="fw-bold mb-2">
                                    Why Fin Made These Changes
                                </h4>

                                <p className="text-muted lh-lg mb-0">
                                    {model_portfolio?.short_reasoning}
                                </p>

                            </div>



                            {/* ALLOCATION CHANGES */}

                            <h4 className="fw-bold mb-3">
                                Allocation Changes
                            </h4>


                            <div className="table-responsive">

                                <table className="table table-hover align-middle">

                                    <thead className="table-light">

                                        <tr>
                                            <th>Ticker</th>
                                            <th>Current</th>
                                            <th>Model</th>
                                            <th>Change</th>
                                        </tr>

                                    </thead>


                                    <tbody>

                                        {model_portfolio?.positions.map(
                                            (position: any) => {

                                                const currentPosition =
                                                    portfolio.find(
                                                        (p: any) =>
                                                            p.ticker ===
                                                            position.ticker
                                                    );


                                                const currentAllocation =
                                                    currentPosition?.allocation ??
                                                    0;


                                                const modelAllocation =
                                                    position.modeled_allocation ??
                                                    position.allocation ??
                                                    0;


                                                const change =
                                                    modelAllocation -
                                                    currentAllocation;


                                                return (

                                                    <tr key={position.ticker}>

                                                        <td className="fw-bold">
                                                            {position.ticker}
                                                        </td>


                                                        <td>

                                                            {(currentAllocation * 100)
                                                                .toFixed(2)}%

                                                        </td>


                                                        <td>

                                                            {(modelAllocation * 100)
                                                                .toFixed(2)}%

                                                        </td>


                                                        <td
                                                            className={
                                                                change > 0
                                                                    ? "text-success fw-semibold"
                                                                    : change < 0
                                                                        ? "text-danger fw-semibold"
                                                                        : "text-muted"
                                                            }
                                                        >

                                                            {change > 0
                                                                ? "+"
                                                                : ""}

                                                            {(change * 100)
                                                                .toFixed(2)}%

                                                        </td>

                                                    </tr>

                                                );

                                            }
                                        )}

                                    </tbody>

                                </table>

                            </div>

                        </div>

                    </div>

                )}



                {/* =====================================================
                    ADVANCED ANALYTICS
                ===================================================== */}

                <div className="mt-5 mb-3">

                    <h2 className="fw-bold mb-1">
                        Advanced Analytics
                    </h2>

                    <p className="text-muted mb-0">
                        Explore relationships between the assets in your portfolio.
                    </p>

                </div>



                {/* CORRELATION */}

                <div className="card border shadow-sm mb-4">

                    <div className="card-body p-4">

                        <h3 className="fw-bold mb-1">
                            Correlation Matrix
                        </h3>

                        <p className="text-muted mb-4">
                            Correlation measures how closely assets move
                            together. Values near +1 indicate similar
                            movement, values near -1 indicate opposite
                            movement, and values near 0 indicate little
                            relationship.
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



                {/* COVARIANCE */}

                <div className="card border shadow-sm">

                    <div className="card-body p-4">

                        <h3 className="fw-bold mb-1">
                            Covariance Matrix
                        </h3>

                        <p className="text-muted mb-4">
                            Covariance measures how two assets move relative
                            to one another. Positive values indicate movement
                            in the same direction, while negative values
                            indicate movement in opposite directions.
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



                {/* =====================================================
                    ASK FIN
                ===================================================== */}

                <div className="mt-5 mb-3">

                    <h2 className="fw-bold mb-1">
                        Ask Fin
                    </h2>

                    <p className="text-muted mb-0">
                        Ask questions about your portfolio, risk,
                        or model allocation.
                    </p>

                </div>



                <div className="card border shadow-sm mb-5">

                    <div className="card-body p-0">


                        {/* CHAT HEADER */}

                        <div className="p-4 border-bottom">

                            <div className="d-flex align-items-center gap-3">

                                <div
                                    className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold"
                                    style={{
                                        width: "42px",
                                        height: "42px"
                                    }}
                                >
                                    F
                                </div>


                                <div>

                                    <h5 className="fw-bold mb-0">
                                        Fin
                                    </h5>

                                    <small className="text-muted">
                                        Portfolio Assistant
                                    </small>

                                </div>

                            </div>

                        </div>



                        {/* MESSAGES */}

                        <div
                            style={{
                                height: "500px",
                                overflowY: "auto"
                            }}
                        >

                            {messages.map((msg: any) => (

                                <div
                                    key={msg.chat_id}
                                    className={`p-4 border-bottom ${msg.role === "assistant"
                                            ? "bg-light"
                                            : "bg-white"
                                        }`}
                                >

                                    <div className="d-flex gap-3">


                                        {/* AVATAR */}

                                        <div
                                            className={`rounded-circle d-flex align-items-center justify-content-center fw-bold ${msg.role === "assistant"
                                                    ? "bg-primary text-white"
                                                    : "bg-dark text-white"
                                                }`}
                                            style={{
                                                width: "36px",
                                                height: "36px",
                                                minWidth: "36px"
                                            }}
                                        >

                                            {msg.role === "assistant"
                                                ? "F"
                                                : "Y"}

                                        </div>



                                        {/* MESSAGE */}

                                        <div className="flex-grow-1">

                                            <div className="fw-semibold mb-2">

                                                {msg.role === "assistant"
                                                    ? "Fin"
                                                    : "You"}

                                            </div>


                                            <ReactMarkdown
                                                remarkPlugins={[
                                                    remarkGfm,
                                                    remarkMath
                                                ]}
                                                rehypePlugins={[
                                                    rehypeKatex
                                                ]}
                                            >

                                                {msg.content}

                                            </ReactMarkdown>

                                        </div>

                                    </div>

                                </div>

                            ))}


                            <div ref={messagesEndRef} />

                        </div>



                        {/* CHAT INPUT */}

                        <div className="p-3 p-md-4 border-top bg-light">

                            <form onSubmit={handleSubmit}>

                                <div className="input-group input-group-lg">

                                    <input
                                        type="text"
                                        className="form-control"
                                        id="fin_box"
                                        value={message}
                                        onChange={(e) =>
                                            setMessage(e.target.value)
                                        }
                                        placeholder="Ask Fin about your portfolio..."
                                    />


                                    <button
                                        type="submit"
                                        className="btn btn-primary px-4"
                                        disabled={!message.trim()}
                                    >
                                        Send
                                    </button>

                                </div>

                            </form>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}