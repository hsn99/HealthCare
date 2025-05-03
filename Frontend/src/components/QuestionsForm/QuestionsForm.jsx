// src/App.js
import React, { useState } from "react"
import axios from "axios"

const abcdeQuestions = [
  {
    section: "Airway",
    questions: [
      {
        en: "Are you having difficulty breathing or swallowing?",
        ar: "هل تعاني من صعوبة في التنفس أو البلع؟",
      },
    ],
  },
  {
    section: "Breathing",
    questions: [
      {
        en: "Are you experiencing shortness of breath?",
        ar: "هل تعاني من ضيق في التنفس؟",
      },
    ],
  },
  {
    section: "Circulation",
    questions: [
      {
        en: "Please measure blood pressure and pulse.",
        ar: "يرجى قياس ضغط الدم والنبض.",
      },
    ],
  },
  {
    section: "Disability",
    questions: [
      {
        en: "Are you feeling confused, or do you have any numbness?",
        ar: "هل تشعر بالارتباك أو هل تعاني من أي خدر؟",
      },
    ],
  },
  {
    section: "Exposure",
    questions: [
      {
        en: "Please measure body temperature.",
        ar: "يرجى قياس درجة حرارة الجسم.",
      },
    ],
  },
]

function QuestionsForm() {
  const [started, setStarted] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState([])
  const [input, setInput] = useState("")
  const [responseData, setResponseData] = useState(null)

  const handleStart = () => {
    setStarted(true)
    setCurrentQuestion(0)
    setAnswers([])
    setInput("")
    setResponseData(null)
  }

  const handleNext = () => {
    const updatedAnswers = [...answers, input]
    setAnswers(updatedAnswers)
    setInput("")

    if (currentQuestion < abcdeQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      // Submit to server
      axios
        .post("http://localhost:8000/questionnaire", {
          answers: updatedAnswers,
        })
        .then((res) => {
          setResponseData(res.data)
          setStarted(false)
        })
        .catch((err) => {
          alert("Error submitting answers")
          console.error(err)
        })
    }
  }

  const handleMeasurement = (section) => {
    if (section === "Circulation") {
      const result = "BP: 120/80, Pulse: 72bpm"
      setInput(result)
    } else if (section === "Exposure") {
      const result = "Temperature: 36.7°C"
      setInput(result)
    }
  }

  const current = abcdeQuestions[currentQuestion]
  const question = current.questions[0]

  return (
    <div style={{ padding: "2rem" }}>
      {responseData ? (
        <div>
          <h2>Test Completed</h2>
          <p>
            <strong>Assigned Doctor:</strong>{" "}
            {responseData.assigned_doctor || "Not Assigned"}
          </p>
          <p>
            <strong>Assigned Room:</strong>{" "}
            {responseData.assigned_room || "Not Assigned"}
          </p>

          <br />
          <button onClick={handleStart}>Restart Test</button>
        </div>
      ) : !started ? (
        <button onClick={handleStart}>Start Test</button>
      ) : (
        <div>
          <h2>{current.section}</h2>
          <h3>{question.en}</h3>
          <h3>{question.ar}</h3>

          {current.section === "Circulation" ||
          current.section === "Exposure" ? (
            <button
              onClick={() => handleMeasurement(current.section)}
              style={{ padding: "0.5rem 1rem", marginTop: "1rem" }}
            >
              Start {current.section} Test
            </button>
          ) : (
            <select
              name="answer"
              id="answer"
              onChange={(e) => setInput(e.target.value)}
              value={input}
            >
              <option value="" disabled>
                Select your answer
              </option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          )}

          <br />
          <br />
          <button onClick={handleNext} disabled={!input}>
            {currentQuestion === abcdeQuestions.length - 1 ? "Submit" : "Next"}
          </button>
        </div>
      )}
    </div>
  )
}

export default QuestionsForm
