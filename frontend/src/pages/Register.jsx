import { useState } from "react";
import { registerUser } from "../api/auth.js";
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });
  const change = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const submit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(form);
      alert("Registration successful");
      navigate("/login");
    } catch (err) {
      err.response?.data?.detail;
    }
  };

  return (
    <div className="container">
      <h1>Register</h1>
      <form onSubmit={submit}>
        <input placeholder="Name" name="name" onChange={change} />
        <input
          placeholder="Email"
          name="email"
          type="email"
          onChange={change}
        />
        <input
          placeholder="Password"
          name="password"
          type="password"
          onChange={change}
        />
        <button>Register</button>
      </form>
      <Link to={"/login"}>Already have an account?</Link>
    </div>
  );
}
