import React, { useState, useEffect } from "react"
import axios from "axios"
import "./QuestionsForm.css"
import welcomeAudio from "../../assets/audio/Welcome.wav"
import airwayAudio from "../../assets/audio/A.wav"
import breathingAudio from "../../assets/audio/B.wav"
import circulationAudio from "../../assets/audio/C.wav"
import disabilityAudio from "../../assets/audio/D.wav"
import exposureAudio from "../../assets/audio/E.wav"
import finalAudio from "../../assets/audio/Final.wav"

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

function QuestionsForm({ handleLogOut }) {
  const [started, setStarted] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState([])
  const [input, setInput] = useState("")
  const [responseData, setResponseData] = useState(null)
  const [measurementResult, setMeasurementResult] = useState("")
  const [bloodPressure, setBloodPressure] = useState("")

  const final = new Audio(finalAudio)

  useEffect(() => {
    if (!started) return

    let section = abcdeQuestions[currentQuestion].section
    let audioPath

    switch (section) {
      case "Airway":
        audioPath = airwayAudio
        break
      case "Breathing":
        audioPath = breathingAudio
        break
      case "Circulation":
        audioPath = circulationAudio
        break
      case "Disability":
        audioPath = disabilityAudio
        break
      case "Exposure":
        audioPath = exposureAudio
        break
      default:
        return
    }

    const audio = new Audio(audioPath)
    audio.play()
  }, [currentQuestion, started])

  const handleStart = () => {
    setStarted(true)
    setCurrentQuestion(0)
    setAnswers([])
    setInput("")
    setResponseData(null)
    setMeasurementResult("")
    setBloodPressure("")
  }

  const patient_id = localStorage.getItem("user_id")

  const handleNext = () => {
    let newAnswers = []

    const section = abcdeQuestions[currentQuestion].section

    if (section === "Circulation") {
      const bp = bloodPressure || "No BP"
      const pulse = measurementResult || "No Pulse"
      newAnswers.push(bp, pulse)
    } else if (section === "Exposure") {
      newAnswers.push(measurementResult || "No Temperature")
    } else {
      newAnswers.push(input || "No answer")
    }

    const updatedAnswers = [...answers, ...newAnswers]

    setAnswers(updatedAnswers)
    setInput("")
    setMeasurementResult("")
    setBloodPressure("")

    if (currentQuestion < abcdeQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      axios
        .post("http://localhost:8000/questionnaire", {
          answers: updatedAnswers,
          patient_id: patient_id,
        })
        .then((res) => {
          setResponseData(res.data)
          setStarted(false)
          final.play()

          setTimeout(() => {
            handleLogOut()
          }, 7000)
        })
        .catch((err) => {
          alert("Error submitting answers")
          console.error(err)
        })
    }
  }

  useEffect(() => {
    const audio = new Audio(welcomeAudio)
    audio.play()
  }, [])

  const handleMeasurement = async (section) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/questionnaire/${section}`
      )

      if (response?.data) {
        setMeasurementResult(response.data.res)
        setInput(response.data.res) // Used to enable the "Next" button
      } else {
        alert("No data received from the server.")
      }
    } catch (error) {
      alert("Error retrieving measurement data.")
      console.error("Measurement error:", error)
    }
  }

  const current = abcdeQuestions[currentQuestion]
  const question = current.questions[0]

  return (
    <div className="form-container">
      {responseData ? (
        <div className="card response">
          <h2>Test Completed</h2>
          <p>
            <strong>Assigned Doctor:</strong>{" "}
            {responseData.assigned_doctor || "Not Assigned"}
          </p>
          <p>
            <strong>Assigned Room:</strong>{" "}
            {responseData.assigned_room || "Not Assigned"}
          </p>
          {/* <button className="button" onClick={handleStart}>
            Restart Test
          </button> */}
        </div>
      ) : !started ? (
        <div className="card center">
          <h2>Start Your Health Check</h2>
          <button className="button" onClick={handleStart}>
            Start Test
          </button>
        </div>
      ) : (
        <div className="card question-card">
          <h2>{current.section}</h2>
          <p className="question-en">{question.en}</p>
          <p className="question-ar">{question.ar}</p>

          {current.section === "Circulation" ||
          current.section === "Exposure" ? (
            <>
              {current.section === "Circulation" && (
                <div className="input-group">
                  <label htmlFor="blood_pressure" className="input-label">
                    Blood Pressure
                  </label>
                  <input
                    type="text"
                    name="blood_pressure"
                    id="blood_pressure"
                    className="text-input"
                    value={bloodPressure}
                    onChange={(e) => setBloodPressure(e.target.value)}
                  />
                </div>
              )}
              <button
                className="button small"
                onClick={() => handleMeasurement(current.section)}
              >
                Start {current.section} Test
              </button>
              <p className="test-result-label">
                {measurementResult || "Result will appear here"}
              </p>
            </>
          ) : (
            <div className="yes-no-buttons">
              <button
                className={`button small yes ${
                  input === "yes" ? "selected yes" : ""
                }`}
                onClick={() => setInput("yes")}
              >
                Yes
              </button>
              <button
                className={`button small no ${
                  input === "no" ? "selected no" : ""
                }`}
                onClick={() => setInput("no")}
              >
                No
              </button>
            </div>
          )}

          <button
            className="button next"
            onClick={handleNext}
            disabled={
              current.section === "Circulation"
                ? !bloodPressure || !measurementResult
                : current.section === "Exposure"
                ? !measurementResult
                : !input
            }
          >
            {currentQuestion === abcdeQuestions.length - 1 ? "Submit" : "Next"}
          </button>
        </div>
      )}
    </div>
  )
}

export default QuestionsForm
