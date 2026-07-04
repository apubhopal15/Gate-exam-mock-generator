import { useState, useEffect } from "react";

export default function Timer({ ontimeup, minutes }) {
  const [secondsleft, setSecondsleft] = useState(minutes * 60);
  useEffect(() => {
    if (secondsleft <= 0) {
      ontimeup();
      return;
    }
    const timer = setInterval(() => {
      setSecondsleft((s) => s - 1);
    }, 1000);
    return () => {
      clearInterval(timer);
    };
  }, [secondsleft]);
  const formatTime = (time) => {
    return time.toString().padStart(2, "0");
  };
  const hrs = Math.floor(secondsleft / 3600);
  const min = Math.floor((secondsleft % 3600) / 60);
  const sec = secondsleft % 60;
  return (
    <div
      style={{
        background: "#2563eb",
        color: "white",
        padding: "10px",
        borderRadius: "6px",
        textAlign: "center",
        marginBottom: "20px",
      }}
    >
      <h3>
        Time Left: {formatTime(hrs)}:{formatTime(min)}:{formatTime(sec)}
      </h3>
    </div>
  );
}
