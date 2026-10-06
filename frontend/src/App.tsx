import { useEffect, useState } from "react";

import {
  getPredictionHistory,
  predictUrl,
  type PredictionHistoryResponse,
  type PredictionResponse,
} from "./services/api";


function App() {
  const [url, setUrl] = useState("");

  const [result, setResult] =
    useState<PredictionResponse | null>(null);

  const [history, setHistory] =
    useState<PredictionHistoryResponse[]>([]);

  const [loading, setLoading] = useState(false);

  const [historyLoading, setHistoryLoading] =
    useState(true);

  const [error, setError] = useState("");


  async function loadHistory() {
    try {
      setHistoryLoading(true);

      const records = await getPredictionHistory();

      setHistory(records);
    } catch (err) {
      console.error("Failed to load history:", err);
    } finally {
      setHistoryLoading(false);
    }
  }


  useEffect(() => {
    loadHistory();
  }, []);


  async function handleAnalyze() {
    if (!url.trim()) {
      setError("Please enter a URL to analyze.");
      setResult(null);
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const prediction = await predictUrl(url.trim());

      setResult(prediction);

      await loadHistory();
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(
          "Something went wrong while analyzing the URL."
        );
      }
    } finally {
      setLoading(false);
    }
  }


  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleString();
  }


  return (
    <div className="app">

      {/* --------------------------------------------------
          Header
      -------------------------------------------------- */}

      <header className="header">
        <div className="brand">

          <div className="logo">
            🛡️
          </div>

          <div>
            <h1>PhishGuard AI</h1>

            <p>
              AI-Powered URL Phishing Detection
            </p>
          </div>

        </div>
      </header>


      {/* --------------------------------------------------
          Main
      -------------------------------------------------- */}

      <main className="main">

        <section className="hero">

          <span className="badge">
            AI SECURITY ANALYZER
          </span>


          <h2>
            Check if a URL is
            <span> potentially dangerous</span>
          </h2>


          <p className="description">
            Analyze suspicious URLs using Machine Learning,
            Deep Learning, and an expert rule system.
          </p>


          {/* --------------------------------------------------
              URL Input
          -------------------------------------------------- */}

          <div className="scan-card">

            <label htmlFor="url">
              Enter a URL to analyze
            </label>


            <div className="input-row">

              <input
                id="url"
                type="text"
                value={url}
                onChange={(event) => {
                  setUrl(event.target.value);
                  setError("");
                }}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleAnalyze();
                  }
                }}
                placeholder="https://example.com"
                disabled={loading}
              />


              <button
                type="button"
                onClick={handleAnalyze}
                disabled={loading}
              >
                {loading
                  ? "⏳ Analyzing..."
                  : "🔍 Analyze URL"}
              </button>

            </div>


            {error && (
              <p className="error-message">
                ⚠️ {error}
              </p>
            )}

          </div>


          {/* --------------------------------------------------
              Prediction Result
          -------------------------------------------------- */}

          {result && (
            <section
              className={`result-card ${result.classification ===
                  "potentially_phishing"
                  ? "result-danger"
                  : "result-safe"
                }`}
            >

              {/* Result Header */}

              <div className="result-header">

                <div>

                  <span className="result-label">
                    ANALYSIS RESULT
                  </span>

                  <h3>
                    {result.classification ===
                      "potentially_phishing"
                      ? "⚠️ Potentially Phishing"
                      : "🟢 Legitimate"}
                  </h3>

                </div>


                {/* Risk Score */}

                <div className="score-box">

                  <span>
                    RISK SCORE
                  </span>

                  <div className="score-number">
                    {result.final_score}
                    <small>/100</small>
                  </div>

                </div>

              </div>


              {/* Risk Bar */}

              <div className="risk-section">

                <div className="risk-label-row">

                  <span>
                    Low Risk
                  </span>

                  <span>
                    High Risk
                  </span>

                </div>


                <div className="risk-bar">

                  <div
                    className="risk-fill"
                    style={{
                      width: `${result.final_score}%`,
                    }}
                  />

                </div>


                <div className="risk-scale">

                  <span>0</span>
                  <span>25</span>
                  <span>50</span>
                  <span>75</span>
                  <span>100</span>

                </div>

              </div>


              {/* AI Metrics */}

              <div className="result-grid">

                <div className="result-stat">

                  <div className="stat-icon">
                    🤖
                  </div>

                  <span>
                    Machine Learning
                  </span>

                  <strong>
                    {(
                      result.ml_probability_phishing * 100
                    ).toFixed(2)}
                    %
                  </strong>

                  <div className="mini-bar">

                    <div
                      style={{
                        width: `${result.ml_probability_phishing *
                          100
                          }%`,
                      }}
                    />

                  </div>

                </div>


                <div className="result-stat">

                  <div className="stat-icon">
                    🧠
                  </div>

                  <span>
                    Deep Learning
                  </span>

                  <strong>
                    {(
                      result.dl_probability_phishing * 100
                    ).toFixed(2)}
                    %
                  </strong>

                  <div className="mini-bar">

                    <div
                      style={{
                        width: `${result.dl_probability_phishing *
                          100
                          }%`,
                      }}
                    />

                  </div>

                </div>


                <div className="result-stat">

                  <div className="stat-icon">
                    🛡️
                  </div>

                  <span>
                    Expert Indicators
                  </span>

                  <strong>
                    {result.indicator_count}
                  </strong>

                  <small>
                    triggered
                  </small>

                </div>

              </div>


              {/* Score Calculation */}

              <div className="calculation-box">

                <h4>
                  Risk Calculation
                </h4>

                <div className="calculation-row">

                  <span>
                    Combined AI probability
                  </span>

                  <strong>
                    {(result.raw_score * 100).toFixed(2)}%
                  </strong>

                </div>


                <div className="calculation-row">

                  <span>
                    Expert indicator boost
                  </span>

                  <strong>
                    +{(result.indicator_boost * 100).toFixed(2)}%
                  </strong>

                </div>


                <div className="calculation-row total">

                  <span>
                    Final risk score
                  </span>

                  <strong>
                    {result.final_score}/100
                  </strong>

                </div>

              </div>


              {/* Analyzed URL */}

              <div className="analyzed-url">

                <span>
                  ANALYZED URL
                </span>

                <p>
                  {result.url}
                </p>

              </div>


              {/* Expert Indicators */}

              {result.triggered_indicators.length > 0 ? (

                <div className="indicators">

                  <h4>
                    🛡️ Expert System Indicators
                  </h4>

                  <p className="indicator-description">
                    These rule-based indicators were detected
                    in the submitted URL.
                  </p>


                  <ul>

                    {result.triggered_indicators.map(
                      (indicator, index) => (

                        <li key={index}>
                          <span>⚠️</span>
                          {indicator}
                        </li>

                      )
                    )}

                  </ul>

                </div>

              ) : (

                <div className="no-indicators">

                  <span>
                    ✓
                  </span>

                  <div>
                    <strong>
                      No expert indicators detected
                    </strong>

                    <p>
                      The rule-based expert system did not
                      identify any suspicious URL patterns.
                    </p>
                  </div>

                </div>

              )}

            </section>
          )}

        </section>


        {/* --------------------------------------------------
            AI Components
        -------------------------------------------------- */}

        <section className="info-grid">

          <div className="info-card">

            <div className="info-icon">
              🤖
            </div>

            <h3>
              Machine Learning
            </h3>

            <p>
              Random Forest analyzes URL characteristics
              extracted from the submitted URL.
            </p>

          </div>


          <div className="info-card">

            <div className="info-icon">
              🧠
            </div>

            <h3>
              Deep Learning
            </h3>

            <p>
              An Artificial Neural Network provides an
              additional phishing probability.
            </p>

          </div>


          <div className="info-card">

            <div className="info-icon">
              🛡️
            </div>

            <h3>
              Expert System
            </h3>

            <p>
              Rule-based indicators identify suspicious
              URL patterns.
            </p>

          </div>

        </section>


        {/* --------------------------------------------------
    Scan Summary
-------------------------------------------------- */}

        <section className="summary-section">

          <div className="summary-heading">

            <div>
              <span className="result-label">
                OVERVIEW
              </span>

              <h2>
                Scan Summary
              </h2>
            </div>

          </div>


          <div className="summary-grid">

            <div className="summary-card">

              <span className="summary-icon">
                🔍
              </span>

              <div>
                <span className="summary-label">
                  Total Scans
                </span>

                <strong>
                  {history.length}
                </strong>
              </div>

            </div>


            <div className="summary-card">

              <span className="summary-icon">
                🟢
              </span>

              <div>
                <span className="summary-label">
                  Legitimate
                </span>

                <strong>
                  {
                    history.filter(
                      (record) =>
                        record.classification ===
                        "legitimate"
                    ).length
                  }
                </strong>
              </div>

            </div>


            <div className="summary-card">

              <span className="summary-icon">
                ⚠️
              </span>

              <div>
                <span className="summary-label">
                  Potentially Phishing
                </span>

                <strong>
                  {
                    history.filter(
                      (record) =>
                        record.classification ===
                        "potentially_phishing"
                    ).length
                  }
                </strong>
              </div>

            </div>

          </div>

        </section>

        {/* --------------------------------------------------
            Prediction History
        -------------------------------------------------- */}

        <section className="history-section">

          <div className="history-heading">

            <div>

              <span className="result-label">
                DATABASE
              </span>

              <h2>
                Recent Scans
              </h2>

            </div>


            <button
              type="button"
              className="refresh-button"
              onClick={loadHistory}
              disabled={historyLoading}
            >
              {historyLoading
                ? "⏳ Loading..."
                : "↻ Refresh"}
            </button>

          </div>


          {historyLoading ? (

            <div className="empty-history">
              Loading scan history...
            </div>

          ) : history.length === 0 ? (

            <div className="empty-history">
              No scans have been recorded yet.
            </div>

          ) : (

            <div className="history-list">

              {history.map((record) => (

                <div
                  className="history-card"
                  key={record.id}
                >

                  <div className="history-main">

                    <div
                      className={
                        record.classification ===
                          "potentially_phishing"
                          ? "history-status danger"
                          : "history-status safe"
                      }
                    >

                      {record.classification ===
                        "potentially_phishing"
                        ? "⚠️ Potentially Phishing"
                        : "🟢 Legitimate"}

                    </div>


                    <p className="history-url">
                      {record.url}
                    </p>


                    <span className="history-date">
                      {formatDate(
                        record.created_at
                      )}
                    </span>

                  </div>


                  <div className="history-score">

                    <span>
                      Risk
                    </span>

                    <strong>
                      {record.final_score}
                    </strong>

                    <small>
                      / 100
                    </small>

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}


export default App;