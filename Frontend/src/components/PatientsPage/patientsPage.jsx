import React, { useEffect, useState } from "react"
import axios from "axios"
import "./patientsPage.css"

function PatientsPage() {
  const [patients, setPatients] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    axios
      .get("http://localhost:8000/patients")
      .then((response) => {
        setPatients(response.data)
        console.log("Patients data:", response.data)
      })
      .catch((err) => {
        console.error("Error fetching patients:", err)
        setError("Failed to load patients.")
      })
  }, [])

  return (
    <div className="patients-container">
      <h2>All Patients</h2>
      {error && <p className="error">{error}</p>}
      <div className="patient-cards-wrapper">
        {patients.map((patient) => (
          <div key={patient.id} className="patient-card">
            <h3>{patient.name}</h3>
            <p>
              <strong>Age:</strong> {patient.age}
            </p>
            <p>
              <strong>Gender:</strong> {patient.gender}
            </p>
            <p>
              <strong>Contact Info:</strong> {patient.contact_info}
            </p>
            <p>
              <strong>Weight:</strong> {patient.weight} kg
            </p>
            <p>
              <strong>Height:</strong> {patient.height} cm
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default PatientsPage
