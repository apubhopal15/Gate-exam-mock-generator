import OptionMcq from "./OptionMcq";
import OptionMsq from "./OptionMsq";
import InputboxNat from "./InputboxNat";

export default function Question({
  question,
  answerOption,
  answerNumeric,
  setAnswerOption,
  setAnswerNumeric,
}) {
  return (
    <div>
      <h3>Q{question.question_order}</h3>
      <p>{question.question_text}</p>
      {question.question_type === "MCQ" && (
        <OptionMcq
          options={question.options || []}
          answer={answerOption}
          setAnswer={setAnswerOption}
        />
      )}
      {question.question_type === "MSQ" && (
        <OptionMsq
          options={question.options || []}
          answer={answerOption}
          setAnswer={setAnswerOption}
        />
      )}
      {question.question_type === "NAT" && (
        <InputboxNat answer={answerNumeric} setAnswer={setAnswerNumeric} />
      )}
    </div>
  );
}
