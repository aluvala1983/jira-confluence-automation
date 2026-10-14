import { useEffect, useState } from "react";

export default function App() {
  const [apiStatus, setApiStatus] = useState("Checking API...");

  useEffect(() => {
    const controller = new AbortController();

    fetch("/api/health", { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`API returned HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((health) => setApiStatus(`API ${health.status}`))
      .catch((error) => {
        if (error.name !== "AbortError") {
          setApiStatus("API unavailable");
        }
      });

    return () => controller.abort();
  }, []);

  return (
    <main>
      <p className="eyebrow">Local prototype</p>
      <h1>Weekly Jira Status Reports</h1>
      <p className="intro">
        A workspace for preparing customer and leadership report drafts.
      </p>
      <section aria-live="polite" className="status">
        <span className="status-dot" aria-hidden="true" />
        {apiStatus}
      </section>
      <p className="note">
        Jira connection and report generation will be added in a later step.
      </p>
    </main>
  );
}
