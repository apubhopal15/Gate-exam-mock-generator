export default function InputboxNat({ answer, setAnswer }) {
  return (
    <input
      type="number"
      step="any"
      value={answer ?? ""}
      onChange={(e) => {
        setAnswer(e.target.value);
      }}
      placeholder="Enter your answer"
    />
  );
}
