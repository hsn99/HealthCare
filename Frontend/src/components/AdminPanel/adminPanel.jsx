import React from "react"
import { useNavigate } from "react-router-dom"

const AdminPanel = () => {
  const navigate = useNavigate()

  const goToAddDoctor = () => {
    navigate("/doctor")
  }

  const goToAddPatient = () => {
    navigate("/patient")
  }

  return (
    <div className="form-container">
      <div className="form-box text-center">
        <h1 className="form-title">Admin Panel</h1>
        <div className="form-grid">
          <button className="submit-btn" onClick={goToAddDoctor}>
            Add Doctor
          </button>
          <button className="submit-btn" onClick={goToAddPatient}>
            Add Patient
          </button>
        </div>
      </div>
    </div>
  )
}

export default AdminPanel
