import type { Position } from "../types/Position";

const API_URL = "http://localhost:8000";

export async function getTicker(ticker: string) {

    const response = await fetch(
        `http://localhost:8000/get_ticker_details/${ticker}`
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(errorData.detail);
    }

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail);
    }

    const data = await response.json();


    return data;
}

export async function analyzePortfolio(portfolio: Position[], username: string, level: string, user_uuid: string) {
    const response = await fetch(
        `${API_URL}/portfolio/analyze`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify({
            portfolio: portfolio,
            username: username,
            level: level,
            user_uuid: user_uuid
        }),

    }
    )
    return await response.json();
}


export async function analyze_portfolio(portfolio: Position[], username: string, level: string, user_uuid: string, on_progress: (node: string) => void, on_complete: (portfolioId: string) => void) {
    const response = await fetch(`${API_URL}/portfolio/analyze`,
        {
            method: "POST",
            headers: {
                "content-type": "application/json",
            },
            body: JSON.stringify({
                portfolio: portfolio,
                username: username,
                level: level,
                user_uuid: user_uuid
            })
        }
    );

    if (!response) {
        throw new Error("No response stream");
    }

    const body = response.body;

    if (!body) {
        throw new Error("No response stream");
    }

    const reader = body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { value, done } = await reader.read();

        if (done) {
            break;
        }

        const chunk = decoder.decode(value, { stream: true });

        const lines = chunk.split("\n");

        for (const line of lines) {
            if (line.startsWith("data: ")) {
                const jsonString = line.slice(6);
                const event = JSON.parse(jsonString);
                if (event.type === "progress") {
                    on_progress(event.node);
                }
                if (event.type === "complete") {
                    on_complete(event.portfolioId);
                }
            }
        }



    }



}


export async function getPortfolio(portfolioId: string) {
    //const response = await fetch(`${API_URL}/getportfolio/${portfolioId}`);
    const response = await fetch(`${API_URL}/endpoint_test/new_data_stream/${portfolioId}`);

    return await response.json();
}

export async function uploadPortfolioFile(file: File) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_URL}/portfolio/upload`,
        {
            method: "POST",
            body: formData
        }
    );

    if (!response.ok) {
        throw new Error("Failed to upload portfolio file");
    }

    return await response.json();
}

export async function SendMessage(message: string, portfolioId: string) {
    const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            portfolioId: portfolioId
        })
    });

    return await response.json();
}