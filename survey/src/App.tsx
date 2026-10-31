import { useState } from "react";

const grableQuestions = [
  {
    id: 1,
    question: "In general, how would your best friend describe you as a risk taker?",
    options: [
      { value: "a", label: "A real gambler" },
      { value: "b", label: "Willing to take risks after completing adequate research" },
      { value: "c", label: "Cautious" },
      { value: "d", label: "A real risk avoider" }
    ]
  },
  {
    id: 2,
    question: "You are on a TV game show and can choose one of the following; which would you take?",
    options: [
      { value: "a", label: "$1,000 in cash" },
      { value: "b", label: "A 50% chance at winning $5,000" },
      { value: "c", label: "A 25% chance at winning $10,000" },
      { value: "d", label: "A 5% chance at winning $100,000" }
    ]
  },
  {
    id: 3,
    question: "You have just finished saving for a “once-in-a-lifetime” vacation. Three weeks before you plan to leave, you lose your job. You would:",
    options: [
      { value: "a", label: "Cancel the vacation" },
      { value: "b", label: "Take a much more modest vacation" },
      { value: "c", label: "Go as scheduled, reasoning that you need the time to prepare for a job search" },
      { value: "d", label: "Extend your vacation, because this might be your last chance to go first-class" }
    ]
  },
  {
    id: 4,
    question: "If you unexpectedly received $20,000 to invest, what would you do?",
    options: [
      { value: "a", label: "Deposit it in a bank account, money market account, or insured CD" },
      { value: "b", label: "Invest it in safe high-quality bonds or bond mutual funds" },
      { value: "c", label: "Invest it in stocks or stock mutual funds" }
    ]
  },
  {
    id: 5,
    question: "In terms of experience, how comfortable are you investing in stocks or stock mutual funds?",
    options: [
      { value: "a", label: "Not at all comfortable" },
      { value: "b", label: "Somewhat comfortable" },
      { value: "c", label: "Very Comfortable" }
    ]
  },
  {
    id: 6,
    question: "When you think of the word “risk,” which of the following words comes to mind first?",
    options: [
      { value: "a", label: "Loss" },
      { value: "b", label: "Uncertainty" },
      { value: "c", label: "Opportunity" },
      { value: "d", label: "Thrill" }
    ]
  },
  {
    id: 7,
    question: "Some experts are predicting prices of assets such as gold, jewels, collectibles, and real estate (hard assets) to increase in value; bond prices may fall, however, experts tend to agree that government bonds are relatively safe. Most of your investment assets are now in high-interest government bonds. What would you do?",
    options: [
      { value: "a", label: "Hold the bonds" },
      { value: "b", label: "Sell the bonds, put half the proceeds into money market accounts, and the other half into hard assets" },
      { value: "c", label: "Sell the bonds and put the total proceeds into hard assets" },
      { value: "d", label: "Sell the bonds, put all the money into hard assets, and borrow additional money to buy more" }
    ]
  },
  {
    id: 8,
    question: "Given the best and worst case returns of the four investment choices below, which would you prefer?",
    options: [
      { value: "a", label: "$200 gain best case; $0 gain/loss worst case" },
      { value: "b", label: "$800 gain best case, $200 loss worst case" },
      { value: "c", label: "$2,600 gain best case, $800 loss worst case" },
      { value: "d", label: "$4,800 gain best case, $2,400 loss worst case" }
    ]
  },
  {
    id: 9,
    question: "In addition to whatever you own, you have been given $1,000. You are now asked to choose between:",
    options: [
      { value: "a", label: "A sure gain of $500" },
      { value: "b", label: "A 50% chance to gain $1,000 and a 50% chance to gain nothing." }
    ]
  },
  {
    id: 10,
    question: "In addition to whatever you own, you have been given $2,000. You are now asked to choose between",
    options: [
      { value: "a", label: "A sure loss of $500" },
      { value: "b", label: "A 50% chance to lose $1,000 and a 50% chance to lose nothing." }
    ]
  },
  {
    id: 11,
    question: "Suppose a relative left you an inheritance of $100,000, stipulating in the will that you invest ALL the money in ONE of the following choices. Which one would you select?",
    options: [
      { value: "a", label: "A savings account or money market mutual fund" },
      { value: "b", label: "A mutual fund that owns stocks and bonds" },
      { value: "c", label: "A portfolio of 15 common stocks" },
      { value: "d", label: "Commodities like gold, silver, and oil" }
    ]
  },
  {
    id: 12,
    question: "If you had to invest $20,000, which of the following investment choices would you find most appealing?",
    options: [
      { value: "a", label: "60% in low-risk investments, 30% in medium-risk investments, 10% in high-risk investments" },
      { value: "b", label: "30% in low-risk investments, 40% in medium-risk investments, 30% in high-risk investments" },
      { value: "c", label: "10% in low-risk investments, 40% in medium-risk investments, 50% in high-risk investments" }
    ]
  },
  {
    id: 13,
    question: "Your trusted friend and neighbor, an experienced geologist, is putting together a group of investors to fund an exploratory gold mining venture. The venture could pay back 50 to 100 times the investment if successful. If the mine is a bust, the entire investment is worthless. Your friend estimates the chance of success is only 20%. If you had the money, how much would you invest?",
    options: [
      { value: "a", label: "Nothing" },
      { value: "b", label: "One month’s salary" },
      { value: "c", label: "Three month’s salary" },
      { value: "d", label: "Six month’s salary" }
    ]
  }
];

export default function App() {
  const [step, setStep] = useState<number>(1);

  const [riskTolerance, setRiskTolerance] = useState<number>(3);
  const [sectorTolerance, setSectorTolerance] = useState<number>(3);
  const [concentrationTolerance, setConcentrationTolerance] = useState<number>(3);
  const [marketReaction, setMarketReaction] = useState<string>("hold");
  const [investmentHorizon, setInvestmentHorizon] = useState<string>("5-10");

  function SliderMarks({ selected }: { selected: number }) {
    return (
      <div className="d-flex justify-content-between px-1 mb-2">
        {[1, 2, 3, 4, 5].map((value) => (
          <span
            key={value}
            className={`small fw-semibold ${selected === value ? "text-primary" : "text-muted"
              }`}
          >
            {value}
          </span>
        ))}
      </div>
    );
  }

  const [grableAnswers, setGrableAnswers] = useState<Record<number, string>>({});

  function setGrableAnswer(question: number, answer: string) {
    setGrableAnswers(prev => ({ ...prev, [question]: answer }));
  }

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
                        <label htmlFor="riskTolerance" className="form-label">
                          How much investment risk are you comfortable taking
                          to achieve higher potential returns?
                        </label>

                        <input
                          id="riskTolerance"
                          type="range"
                          className="form-range mb-0"
                          min={1}
                          max={5}
                          step={1}
                          value={riskTolerance}
                          onChange={(e) =>
                            setRiskTolerance(Number(e.target.value))
                          }
                        />

                        <SliderMarks selected={riskTolerance} />

                        <div className="d-flex justify-content-between small text-muted">
                          <span>Very Conservative</span>
                          <span>Neutral</span>
                          <span>Very Aggressive</span>
                        </div>
                      </div>

                      {/* Question 2 */}
                      <div>
                        <label htmlFor="sectorTolerance" className="form-label">
                          How comfortable are you having a large portion
                          of your portfolio invested in one industry?
                        </label>

                        <input
                          id="sectorTolerance"
                          type="range"
                          className="form-range mb-0"
                          min={1}
                          max={5}
                          step={1}
                          value={sectorTolerance}
                          onChange={(e) =>
                            setSectorTolerance(Number(e.target.value))
                          }
                        />

                        <SliderMarks selected={sectorTolerance} />

                        <div className="d-flex justify-content-between small text-muted">
                          <span>Very Uncomfortable</span>
                          <span>Neutral</span>
                          <span>Very Comfortable</span>
                        </div>
                      </div>

                      {/* Question 3 */}
                      <div>
                        <label htmlFor="concentrationTolerance" className="form-label">
                          How comfortable are you with a significant
                          portion of your portfolio invested in a
                          small number of companies?
                        </label>

                        <input
                          id="concentrationTolerance"
                          type="range"
                          className="form-range mb-0"
                          min={1}
                          max={5}
                          step={1}
                          value={concentrationTolerance}
                          onChange={(e) =>
                            setConcentrationTolerance(Number(e.target.value))
                          }
                        />

                        <SliderMarks selected={concentrationTolerance} />

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
                          { value: "sell_most", label: "Sell most of my investments" },
                          { value: "sell_some", label: "Sell some investments to reduce risk" },
                          { value: "hold", label: "Hold my investments and wait for recovery" },
                          { value: "buy_more", label: "Invest more while prices are lower" }
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
                          { value: "0-1", label: "Within 1 year" },
                          { value: "1-3", label: "1–3 years" },
                          { value: "3-5", label: "3–5 years" },
                          { value: "5-10", label: "5–10 years" },
                          { value: "10+", label: "More than 10 years" }
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
                      Grable–Lytton Risk Assessment
                    </h4>

                    <p className="text-muted mb-4">
                      Complete the following established financial risk tolerance questionnaire.
                    </p>

                    <div className="d-flex flex-column gap-4">
                      {grableQuestions.map((question) => (
                        <fieldset key={question.id} className="border-0 p-0 m-0">
                          <legend className="form-label fs-6">
                            <span className="fw-semibold">{question.id}. </span>
                            {question.question}
                          </legend>

                          {question.options.map((option) => (
                            <div className="form-check" key={option.value}>
                              <input
                                className="form-check-input"
                                type="radio"
                                name={`grable-${question.id}`}
                                id={`grable-${question.id}-${option.value}`}
                                value={option.value}
                                checked={grableAnswers[question.id] === option.value}
                                onChange={() => setGrableAnswer(question.id, option.value)}
                              />
                              <label
                                className="form-check-label"
                                htmlFor={`grable-${question.id}-${option.value}`}
                              >
                                {option.label}
                              </label>
                            </div>
                          ))}
                        </fieldset>
                      ))}
                    </div>
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