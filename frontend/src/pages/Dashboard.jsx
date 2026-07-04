import { useState, useEffect } from "react";
import { data, useNavigate } from "react-router-dom";
import { getMe } from "../api/auth.js";
import Navbar from "../components/Navbar.jsx";
import { getDashboard } from "../api/attempt.js";

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const navigate = useNavigate();

  const load = async () => {
    try {
      const data = await getMe();
      setUser(data);
    } catch (err) {
      localStorage.removeItem("token");
      navigate("/login");
    }
  };
  const loadDashboard = async () => {
    try {
      const data = await getDashboard();
      setDashboard(data);
    } catch (err) {
      localStorage.removeItem("token");
      navigate("/login");
    }
  };

  useEffect(() => {
    load();
    loadDashboard();
  }, []);

  useEffect(() => {}, [dashboard]);
  if (!dashboard) {
    return <h2>Loading...</h2>;
  }

  return (
    <>
      <Navbar />
      {user && <h2 style={{ marginLeft: "10px" }}>Hello {user.user_name},</h2>}
      <div className="container">
        <h1>Dashboard</h1>
        <div>
          <h3>Total attempts: {dashboard.summary.total_attempts}</h3>
          <h3>Completed: {dashboard.summary.completed_attempts}</h3>
          <h3>Average score: {dashboard.summary.avg_score}</h3>
          <h3>Best score: {dashboard.summary.best_score}</h3>
        </div>
        <button onClick={() => navigate("/exams")}>Generate Mock Test</button>
      </div>
    </>
  );
}
