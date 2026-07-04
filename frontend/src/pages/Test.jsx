import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getMock } from "../api/exam";
import Navbar from "../components/Navbar";
import Timer from "../components/Timer";
import { saveAnswer, startAttempt, submitAttempt } from "../api/attempt";
import Question from "../components/Question";

export default function Test() {
  const { mockId } = useParams();
  const navigate = useNavigate();
  const [mock, setMock] = useState(null);
  const [attemptId, setAttemptId] = useState(null);
  const [current, setCurrent] = useState(0);
  const [answerOption, setAnswerOption] = useState({});
  const [answerNumeric, setAnswerNumeric] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const loadTest = async () => {
    try {
      const mockData = await getMock(mockId);
      setMock(mockData);
      const attempt = await startAttempt(mockId);
      setAttemptId(attempt.attempt_id);
    } catch (err) {
      alert("Unable to load test");
    }
  };

  useEffect(() => {
    loadTest();
  }, [mockId]);

  if (!mock?.questions) {
    return <h2>Loading...</h2>;
  }

  const currentQuestion = mock.questions[current];

  const selectAnswerOption = async (optionLabel) => {
    const updated = {
      ...answerOption,
      [currentQuestion.question_id]: optionLabel,
    };
    setAnswerOption(updated);
    try {
      await saveAnswer(attemptId, {
        question_id: currentQuestion.question_id,
        selected_option: optionLabel,
      });
    } catch (err) {
      alert("Autosave Answer Failed");
    }
  };

  const selectAnswerNumeric = async (value) => {
    const number = Number(value);
    const updated = { ...answerNumeric, [currentQuestion.question_id]: number };
    setAnswerNumeric(updated);
    try {
      await saveAnswer(attemptId, {
        question_id: currentQuestion.question_id,
        answer_numeric: number,
      });
    } catch (err) {
      alert("Autosave answer failed");
    }
  };

  const previous = () => {
    if (current > 0) {
      setCurrent(current - 1);
    }
  };

  const next = () => {
    if (current < mock.questions.length - 1) {
      setCurrent(current + 1);
    }
  };

  const submitTest = async () => {
    if (submitting) return;
    setSubmitting(true);
    try {
      const res = await submitAttempt(attemptId);
      navigate(`/result/${attemptId}`);
      setSubmitting(false);
    } catch (err) {
      setSubmitting(false);
    }
  };
  const clearAnswer = async () => {
    const qid = currentQuestion.question_id;
    try {
      if (currentQuestion.question_type === "MCQ") {
        setAnswerOption((prev) => ({
          ...prev,
          [qid]: [],
        }));

        await saveAnswer(attemptId, {
          question_id: qid,
          selected_option: [],
        });
      } else if (currentQuestion.question_type === "MSQ") {
        setAnswerOption((prev) => ({
          ...prev,
          [qid]: [],
        }));

        await saveAnswer(attemptId, {
          question_id: qid,
          selected_option: [],
        });
      } else if (currentQuestion.question_type === "NAT") {
        setAnswerNumeric((prev) => ({
          ...prev,
          [qid]: null,
        }));

        await saveAnswer(attemptId, {
          question_id: qid,
          answer_numeric: null,
        });
      }
    } catch (err) {
      alert("Failed to clear answer");
    }
  };
  return (
    <>
      <Navbar />
      <h2>{mock.title}</h2>
      <div className="container">
        <Timer
          ontimeup={() => {
            submitTest();
          }}
          minutes={mock.duration}
        />
        <Question
          question={currentQuestion}
          answerNumeric={answerNumeric[currentQuestion.question_id]}
          answerOption={answerOption[currentQuestion.question_id]}
          setAnswerNumeric={selectAnswerNumeric}
          setAnswerOption={selectAnswerOption}
        />
        <br></br>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "20px",
          }}
        >
          <button onClick={clearAnswer}>Clear Answer</button>
          <button disabled={current === 0} onClick={previous}>
            Previous
          </button>
          <button
            disabled={current === mock.questions.length - 1}
            onClick={next}
          >
            Next
          </button>
        </div>
        <br></br>
        <button
          onClick={submitTest}
          style={{
            background: "green",
          }}
        >
          Submit
        </button>
        <hr></hr>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(10,1fr)",
            gap: 8,
          }}
        >
          {mock.questions.map((q, index) => {
            const isAnswered =
              answerOption[q.question_id] !== undefined ||
              answerNumeric[q.question_id] !== undefined;

            return (
              //
              // className={
              // index===current
              // ?"current"
              // :answers[q.question_id]
              // ?"correct"
              // :"unanswered"
              // }

              <button
                key={q.question_id}
                onClick={() => setCurrent(index)}
                style={{
                  background: isAnswered ? "green" : "#ddd",
                  color: "black",
                  padding: "6px",
                  borderRadius: "4px",
                }}
              >
                {index + 1}
              </button>
            );
          })}
        </div>
      </div>
    </>
  );
}
