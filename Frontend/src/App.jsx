import React, { useState, useEffect } from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import "./App.css"
import Home from "./components/HomePage/homepage"
import Nav from "./components/Nav/Nav"
import QuestionsForm from "./components/QuestionsForm/QuestionsForm"
import PatientForm from "./components/PatientForm/patientForm"

function App() {
  const [user, setUser] = useState(null)

  const handleLogOut = () => {
    setUser(null)
    localStorage.clear()
    window.location.href = "/"
  }

  useEffect(() => {
    const userId = localStorage.getItem("user_id")
    const userName = localStorage.getItem("user_name")
    if (userId && userName) {
      setUser({ id: userId, name: userName })
    }
  }, [])

  return (
    <Router>
      <div className="App">
        <header>
          <Nav user={user} handleLogOut={handleLogOut} />
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home setUser={setUser} />} />
            <Route path="/test" element={<QuestionsForm />} />
            <Route path="/patient" element={<PatientForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
