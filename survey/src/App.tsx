
import { useState } from "react";

export default function App() {
  const [step, setStep] = useState<number>(1);

  const [riskTolerance, setRiskTolerance] = useState<number>(3);
  const [sectorTolerance, setSectorTolerance] = useState<number>(3);
  const [concentrationTolerance, setConcentrationTolerance] = useState<number>(3);
  const [marketReaction, setMarketReaction] = useState<string>("hold");
  const [investmentHorizon, setInvestmentHorizon] = useState<string>("5-10");

  return (
    <div className="container-fluid bg-light min-vh-100">
      <div className="container py-4">

        <div className="text-center mb-4 mt-4">
          <h1 className="fw-bold mb-2">
            FinLab Research
          </h1>

          <p className="text-muted mb-0">
            Investor Risk Tolerance Study
          </p>
        </div>

        <div className="row justify-content-center">
          <div className="col-lg-10 col-xl-11">

            <div className="card shadow-sm border-0 rounded-4 mb-4">
              <div className="card-body p-4 p-md-5">

                <div className="text-center mb-4">
                  <h2 className="fw-bold mb-2">
                    Financial Risk Assessment
                  </h2>

                  <p className="text-muted mb-0">
                    Help us understand how individuals evaluate
                    investment risk and make financial decisions.
                  </p>
                </div>

                <div className="progress mb-4" style={{ height: "8px" }}>
                  <div
                    className="progress-bar"
                    style={{ width: `${(step / 3) * 100}%` }}
                  />
                </div>

                <p className="text-muted small text-center mb-4">
                  Section {step} of 3
                </p>

                <hr className="my-4" />

                {step === 1 && (
                  <div>
                    <h4 className="fw-bold mb-3">
                      FinLab Risk Questionnaire
                    </h4>

                    <p className="text-muted mb-4">
                      Answer the following questions to help us
                      understand your investment risk tolerance.
                    </p>

                    <div className="d-flex flex-column gap-4">

                      {/* Question 1 */}
                      <div>
                        <label
                          htmlFor="riskTolerance"
                          className="form-label"
                        >
                          How much investment risk are you comfortable taking
                          to achieve higher potential returns?
                        </label>

                        <input
                          id="riskTolerance"
                          type="range"
                          className="form-range"
                          min={1}
                          max={5}
                          step={1}
                          value={riskTolerance}
                          onChange={(e) =>
                            setRiskTolerance(Number(e.target.value))
                          }
                        />

                        <div className="d-flex justify-content-between small text-muted">
                          <span>Very Conservative</span>
                          <span>Neutral</span>
                          <span>Very Aggressive</span>
                        </div>
                      </div>

                      {/* Question 2 */}
                      <div>
                        <label
                          htmlFor="sectorTolerance"
                          className="form-label"
                        >
                          How comfortable are you having a large portion
                          of your portfolio invested in one industry?
                        </label>

                        <input
                          id="sectorTolerance"
                          type="range"
                          className="form-range"
                          min={1}
                          max={5}
                          step={1}
                          value={sectorTolerance}
                          onChange={(e) =>
                            setSectorTolerance(Number(e.target.value))
                          }
                        />

                        <div className="d-flex justify-content-between small text-muted">
                          <span>Very Uncomfortable</span>
                          <span>Neutral</span>
                          <span>Very Comfortable</span>
                        </div>
                      </div>

                      {/* Question 3 */}
                      <div>
                        <label
                          htmlFor="concentrationTolerance"
                          className="form-label"
                        >
                          How comfortable are you with a significant
                          portion of your portfolio invested in a
                          small number of companies?
                        </label>

                        <input
                          id="concentrationTolerance"
                          type="range"
                          className="form-range"
                          min={1}
                          max={5}
                          step={1}
                          value={concentrationTolerance}
                          onChange={(e) =>
                            setConcentrationTolerance(Number(e.target.value))
                          }
                        />

                        <div className="d-flex justify-content-between small text-muted">
                          <span>Very Uncomfortable</span>
                          <span>Neutral</span>
                          <span>Very Comfortable</span>
                        </div>
                      </div>

                      {/* Question 4 */}
                      <div>
                        <label className="form-label">
                          How would you react if your portfolio lost 25% of its
                          value over a few months?
                        </label>

                        {[
                          {
                            value: "sell_most",
                            label: "Sell most of my investments"
                          },
                          {
                            value: "sell_some",
                            label: "Sell some investments to reduce risk"
                          },
                          {
                            value: "hold",
                            label: "Hold my investments and wait for recovery"
                          },
                          {
                            value: "buy_more",
                            label: "Invest more while prices are lower"
                          }
                        ].map((option) => (
                          <div className="form-check" key={option.value}>
                            <input
                              className="form-check-input"
                              type="radio"
                              name="marketReaction"
                              id={option.value}
                              value={option.value}
                              checked={marketReaction === option.value}
                              onChange={(e) =>
                                setMarketReaction(e.target.value)
                              }
                            />

                            <label
                              className="form-check-label"
                              htmlFor={option.value}
                            >
                              {option.label}
                            </label>
                          </div>
                        ))}
                      </div>

                      {/* Question 5 */}
                      <div>
                        <label className="form-label">
                          When do you expect to need a significant portion
                          of the money in this portfolio?
                        </label>

                        {[
                          {
                            value: "0-1",
                            label: "Within 1 year"
                          },
                          {
                            value: "1-3",
                            label: "1–3 years"
                          },
                          {
                            value: "3-5",
                            label: "3–5 years"
                          },
                          {
                            value: "5-10",
                            label: "5–10 years"
                          },
                          {
                            value: "10+",
                            label: "More than 10 years"
                          }
                        ].map((option) => (
                          <div className="form-check" key={option.value}>
                            <input
                              className="form-check-input"
                              type="radio"
                              name="investmentHorizon"
                              id={`horizon-${option.value}`}
                              value={option.value}
                              checked={investmentHorizon === option.value}
                              onChange={(e) =>
                                setInvestmentHorizon(e.target.value)
                              }
                            />

                            <label
                              className="form-check-label"
                              htmlFor={`horizon-${option.value}`}
                            >
                              {option.label}
                            </label>
                          </div>
                        ))}
                      </div>

                    </div>
                  </div>
                )}

                {step === 2 && (
                  <div>
                    <h4 className="fw-bold mb-3">
                      Financial Risk Tolerance Assessment
                    </h4>

                    <p className="text-muted">
                      Complete the following established
                      financial risk tolerance questionnaire.
                    </p>

                    {/* Grable-Lytton Questions */}
                  </div>
                )}

                {step === 3 && (
                  <div>
                    <h4 className="fw-bold mb-3">
                      Portfolio Evaluation
                    </h4>

                    <p className="text-muted">
                      Review hypothetical investment portfolios
                      and evaluate their risk and suitability.
                    </p>

                    {/* Portfolio Scenarios */}
                  </div>
                )}

                <hr className="my-4" />

                <div className="d-flex justify-content-between">
                  <button
                    type="button"
                    className="btn btn-outline-primary"
                    disabled={step === 1}
                    onClick={() => setStep(step - 1)}
                  >
                    Previous
                  </button>

                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={() => {
                      if (step < 3) {
                        setStep(step + 1);
                      }
                    }}
                  >
                    {step === 3 ? "Submit Survey" : "Continue"}
                  </button>
                </div>

              </div>
            </div>

          </div>
        </div>

        <footer className="text-center py-4 mt-5">
          <p className="text-muted small mb-0">
            © {new Date().getFullYear()} FinLab.
            Research conducted for educational purposes.
          </p>
        </footer>

      </div>
    </div>
  );
}
