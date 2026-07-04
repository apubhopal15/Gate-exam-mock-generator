import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { getAnalytics, getResult } from "../api/attempt";

export default function Result() {
  const navigate = useNavigate();
  const { attemptId } = useParams();
  const [score, setScore] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    loadResult();
  }, []);

  const loadResult = async () => {
    try {
      const result = await getResult(attemptId);
      setScore(result.score);
      const report = await getAnalytics(attemptId);
      setAnalytics(report);
    } catch (err) {
      alert("Unable to load result");
    }
  };
  if (!analytics) {
    return <h2>Loading...</h2>;
  }
  return (
    <>
      <Navbar />
      <div className="container">
        <h1>Result</h1>
        <h2>Score: {score}</h2>
        <hr></hr>
        <h1>Analytics</h1>
        {Object.entries(analytics).map(([key, value]) => (
          <p key={key}>
            <strong>{key}</strong>:{String(value)}
          </p>
        ))}
        <br></br>
        <button
          onClick={() => {
            navigate("/dashboard");
          }}
        >
          Dashboard
        </button>
      </div>
    </>
  );
}
