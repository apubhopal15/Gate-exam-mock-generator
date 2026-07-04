export default function OptionMcq({ options = [], answer, setAnswer }) {
  if (!Array.isArray(options)) {
    return <div>No options found</div>;
  }
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
            type="radio"
            name="mcq"
            style={{ width: "16px", height: "16px" }}
            onChange={() => {
              setAnswer([option.option_label]);
            }}
            checked={answer?.includes(option.option_label)}
            value={option.option_label}
          />
          {option.option_label}.{option.option_text}
        </label>
      ))}
    </div>
  );
}
