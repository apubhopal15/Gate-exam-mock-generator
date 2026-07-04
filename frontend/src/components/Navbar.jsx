import { useNavigate, NavLink } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };
  return (
    <nav className="navbar">
      <div className="logo">Gate Mock Exam</div>
      <div className="nav-links">
        <NavLink to="/dashboard" style={{ color: "white", marginRight: 20 }}>
          Dashboard
        </NavLink>
        <NavLink to="/exams" style={{ color: "white", marginRight: 20 }}>
          Exams
        </NavLink>
        <NavLink to="/history" style={{ color: "white" }}>
          History
        </NavLink>
        <button
          onClick={logout}
          style={{
            width: 100,
            background: "crimson",
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
