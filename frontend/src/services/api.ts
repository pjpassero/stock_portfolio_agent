import type { Position } from "../types/Position";

const API_URL = "http://localhost:8000";

export async function getTicker(ticker: string) {

    const response = await fetch(
        `http://localhost:8000/get_ticker_details/${ticker}`
    );

    if (!response.ok) {
        throw new Error("Request failed");
    }

    const data = await response.json();

    console.log(data);

    return data;
}

export async function analyzePortfolio(portfolio: Position[]) {
    const response = await fetch(
        `${API_URL}/portfolio/analyze`, {
        method: "POSt",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(portfolio),

    }
    )
    return await response.json();
}