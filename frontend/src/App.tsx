import { useState } from "react";
import { analyzeTicker } from "./services/api";

function App() {

  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {

    setLoading(true);

    try {
      const data = await analyzeTicker(ticker);

      setResult(data);
    }
    catch (err) {
      console.error(err);
    }

    setLoading(false);
  }

  return (
    <div className="container mt-5">

      <h1>StockAgent</h1>

      <div className="input-group mt-4">

        <input
          className="form-control"
          placeholder="Enter ticker..."
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />

        <button
          className="btn btn-primary"
          onClick={handleAnalyze}
        >
          Analyze
        </button>

      </div>

      {loading && (
        <p className="mt-3">Loading...</p>
      )}

      {result && (

        <div className="card mt-4">

          <div className="card-body">

            <h3>{result.company_name}</h3>

            <p>
              <strong>Ticker:</strong> {result.ticker}
            </p>

            <p>
              <strong>Sector:</strong> {result.sector}
            </p>

            <p>
              <strong>Current Price:</strong> ${result.current_price}
            </p>

            <hr />

            <h5>AI Summary</h5>

            <p>{result.summary}</p>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;