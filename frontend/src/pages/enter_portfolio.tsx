import { useState } from "react";
import { getTicker } from '../services/api'



export default function EnterPortfolio() {
    async function handleAnalyze() {

        try {

            const result = await getTicker(ticker);

            setPrice(result.price);

        } catch (err) {

            console.error(err);

        }

    }
    const [ticker, setTicker] = useState("None");
    const [price, setPrice] = useState("");



    return (
        <div className="container-fluid">
            <div className="row justify-content-center m-5">
                <div className="col-md-10 justify-content-center">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Stock Ticker</th>
                                <th>Share Count</th>
                                <th>Cost Basis</th>
                                <th>Current Value</th>
                            </tr>
                        </thead>
                    </table>
                </div>
            </div>
            <div className="row justify-content-center">
                <div className="col-md-10 mt-5">
                    <div className="card">
                        <div className="card-body justify-content-center">
                            <div className="card-title text-center">
                                <h3>{ticker}</h3>
                            </div>
                            <hr />
                            <form>
                                <div className="form-group justify-content-center">
                                    <input type="text" className="form-control m-1" value={ticker} onChange={(e) => setTicker(e.target.value)} placeholder="Enter Ticker" />
                                    <input type="text" className="form-control m-1" placeholder="Enter Share Amount" />
                                    <input type="text" className="form-control m-1" placeholder="Enter Purchase Price" />
                                    <button type="button" onClick={handleAnalyze} className="btn btn-primary mb-2">Confirm identity</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div >
    );
}