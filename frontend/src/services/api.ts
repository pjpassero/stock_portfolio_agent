const API_URL = "http://localhost:8000";

export async function analyzeTicker(ticker: string) {
    const response = await fetch(
        `${API_URL}/analyze/${ticker}`
    );

    if (!response.ok) {
        throw new Error("Failed to analyze ticker.");
    }

    return response.json();
}