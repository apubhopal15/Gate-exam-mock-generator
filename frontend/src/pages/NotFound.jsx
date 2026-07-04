import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="container">
      <h1>404</h1>
      <h1>Page Not Found</h1>
      <Link to={"/dashboard"}>Go to Home</Link>
    </div>
  );
}
