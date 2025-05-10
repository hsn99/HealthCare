import React, { useState, useEffect } from "react"
import axios from "axios"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import "./App.css"
import Home from "./components/HomePage/homepage"
import Nav from "./components/Nav/Nav"
import QuestionsForm from "./components/QuestionsForm/QuestionsForm"
import PatientForm from "./components/PatientForm/patientForm"
import DoctorForm from "./components/DoctorForm/doctorForm"
import AdminPanel from "./components/AdminPanel/adminPanel"

function App() {
  const [user, setUser] = useState(null)

  const handleLogOut = () => {
    setUser(null)
    localStorage.clear()

    axios
      .post("http://localhost:8000/logout")
      .then((response) => {
        console.log("Logout successful:", response.data)
        window.location.href = "/"
      })
      .catch((error) => {
        console.error("Error during logout:", error)
      })
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
            <Route
              path="/test"
              element={<QuestionsForm handleLogOut={handleLogOut} />}
            />
            <Route path="/patient" element={<PatientForm />} />
            <Route path="/doctor" element={<DoctorForm />} />
            <Route path="/admin-panel" element={<AdminPanel />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
