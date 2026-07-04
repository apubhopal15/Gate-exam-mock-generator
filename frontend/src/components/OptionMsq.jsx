export default function OptionMsq({ options = [], answer = [], setAnswer }) {
  const toggleOption = (option_label) => {
    if (answer.includes(option_label)) {
      setAnswer(answer.filter((x) => x !== option_label));
    } else {
      setAnswer([...answer, option_label]);
    }
  };
  return (
    <div>
      {options.map((option) => (
        <label
          key={option.option_id}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "10px",
            padding: "8px",
            cursor: "pointer",
          }}
        >
          <input
            type="checkbox"
            style={{ width: "16px", height: "16px" }}
            onChange={() => {
              toggleOption(option.option_label);
            }}
            checked={answer.includes(option.option_label)}
          />
          {option.option_label}.{option.option_text}
        </label>
      ))}
    </div>
  );
}
