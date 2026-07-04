import { useEffect, useState } from "react";
import { getHistory } from "../api/attempt";
import Navbar from "../components/Navbar";

export default function History() {
  const [history, setHistory] = useState(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    loadHistory();
  }, [page]);

  const loadHistory = async () => {
    try {
      const data = await getHistory(page, 10);
      setHistory(data);
    } catch (err) {
      alert("Unable to load history");
    }
  };
  if (!history) {
    return <h2>Loading...</h2>;
  }
  return (
    <>
      <Navbar />
      <div className="container">
        <h1>Attempt History</h1>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Mock</th>
              <th>Score</th>
              <th>Status</th>
              <th>Started</th>
            </tr>
          </thead>
          <tbody>
            {history.attempts.map((a) => (
              <tr key={a.attempt_id}>
                <td>{a.attempt_id}</td>
                <td>{a.mocktest_id}</td>
                <td>{a.score}</td>
                <td>{a.status}</td>
                <td>{a.started_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <br></br>
        <button onClick={() => setPage(page - 1)} disabled={page === 1}>
          Previous
        </button>
        <button onClick={() => setPage(page + 1)}>Next</button>
      </div>
    </>
  );
}
