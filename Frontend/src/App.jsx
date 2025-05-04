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
  }

  const checkToken = async () => {
    const user = await CheckSession()
    setUser(user)
  }

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (token) {
      checkToken()
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
            <Route path="/" element={<Home />} />
            <Route path="/test" element={<QuestionsForm />} />
            <Route path="/patient" element={<PatientForm />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
