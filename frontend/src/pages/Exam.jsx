import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generateMock } from "../api/exam";
import Navbar from "../components/Navbar";

export default function Exam() {
  const [exam, setExam] = useState("CSE");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const createMock = async () => {
    setLoading(true);
    try {
      const mock = await generateMock(exam);
      navigate(`/mocks/${mock.id}`);
    } catch (err) {
      alert("Unable to generate mock");
    }
    setLoading(false);
  };
  return (
    <>
      <Navbar />
      <div className="container">
        <h1>Select Exam</h1>
        <select value={exam} onChange={(event) => setExam(event.target.value)}>
          <option value="CSE">CSE</option>
          <option value="DA">DA</option>
        </select>
        <button onClick={createMock}>
          {loading ? "Generating..." : "Generate Mock"}
        </button>
      </div>
    </>
  );
}
