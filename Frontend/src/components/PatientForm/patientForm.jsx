import React, { useState } from "react"
import axios from "axios"
import "./PatientForm.css"

const PatientForm = () => {
  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    height: "",
    contact_info: "",
  })

  const [fingerprintId, setFingerprintId] = useState(null)
  const [isScanning, setIsScanning] = useState(false)
  const [scanError, setScanError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const [submitError, setSubmitError] = useState("")
  const [scanStage, setScanStage] = useState("")

  const [weightResult, setWeightResult] = useState(null)
  const [weightError, setWeightError] = useState("")
  const [isWeightMeasuring, setIsWeightMeasuring] = useState(false)

  const handleMeasureWeight = async () => {
    setIsWeightMeasuring(true)
    setWeightError("")
    setWeightResult(null)

    try {
      const res = await axios.post("http://localhost:8000/patients/weight")
      setWeightResult(res.data.weight)
    } catch (err) {
      console.error(err)
      setWeightError("❌ Failed to measure weight.")
    } finally {
      setIsWeightMeasuring(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleScanFingerprint = async () => {
    setIsScanning(true)
    setScanError("")
    setSuccessMessage("")
    setScanStage("📍 Place your finger on the scanner...")

    try {
      await new Promise((resolve) => setTimeout(resolve, 3000))
      setScanStage("✋ Remove and place your finger again...")

      await new Promise((resolve) => setTimeout(resolve, 1500))

      const res = await axios.post("http://localhost:8000/patients/enroll")
      setFingerprintId(res.data.fingerprint_id)
      setScanStage("✅ Fingerprint added successfully!")
    } catch (err) {
      console.error(err)
      setScanError("❌ Fingerprint scanning failed.")
      setScanStage("")
    } finally {
      setIsScanning(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitError("")
    setSuccessMessage("")
    setScanStage("")

    try {
      const payload = {
        ...form,
        fingerprint_id: fingerprintId,
        age: Number(form.age) || 0,
        weight: weightResult || 0,
        height: Number(form.height) || 0,
      }

      await axios.post("http://localhost:8000/patients", payload)

      setSuccessMessage("✅ Patient added successfully!")

      setTimeout(() => {
        setForm({
          name: "",
          age: "",
          gender: "",
          height: "",
          contact_info: "",
        })
        setFingerprintId(null)
        setScanStage("")
        setWeightResult(null)
      }, 2000)
    } catch (err) {
      console.error(err)
      setSubmitError("❌ Failed to create patient.")
    }
  }

  const isFormValid = form.name && form.age && form.gender && fingerprintId

  return (
    <div className="patient-form-container">
      <div className="form-box">
        <h2 className="form-title">🩺 Add New Patient</h2>

        <form onSubmit={handleSubmit} className="form-grid">
          <div className="form-fields">
            <input
              name="name"
              placeholder="Full Name"
              value={form.name}
              onChange={handleChange}
              className="input-style"
              required
            />
            <input
              type="number"
              name="age"
              placeholder="Age"
              value={form.age}
              onChange={handleChange}
              className="input-style"
              required
            />
            <select
              name="gender"
              value={form.gender}
              onChange={handleChange}
              className="input-style"
              required
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>

            <div className="weight-section">
              <button
                type="button"
                onClick={handleMeasureWeight}
                disabled={isWeightMeasuring}
                className={`measure-btn ${
                  isWeightMeasuring ? "btn-disabled" : ""
                }`}
              >
                {isWeightMeasuring
                  ? "Measuring Weight..."
                  : "🔍 Measure Weight"}
              </button>

              {weightResult && (
                <div className="weight-result">
                  <strong>Weight: </strong>
                  {weightResult} kg
                </div>
              )}

              {weightError && <span className="error-text">{weightError}</span>}
            </div>

            <input
              type="number"
              name="height"
              placeholder="Height (cm)"
              value={form.height}
              onChange={handleChange}
              className="input-style"
            />
            <input
              name="contact_info"
              placeholder="Contact Info"
              value={form.contact_info}
              onChange={handleChange}
              className="input-style"
            />
          </div>

          <div className="scan-section">
            <button
              type="button"
              onClick={handleScanFingerprint}
              disabled={isScanning || !(form.name && form.age && form.gender)}
              className={`scan-btn ${
                isScanning || !(form.name && form.age && form.gender)
                  ? "btn-disabled"
                  : ""
              }`}
            >
              {isScanning ? "Scanning..." : "🔍 Scan Fingerprint"}
            </button>

            {scanStage && (
              <div className="scan-stage-animation">{scanStage}</div>
            )}
            {scanError && <span className="error-text">{scanError}</span>}
          </div>

          <button
            type="submit"
            disabled={!isFormValid}
            className={`submit-btn ${!isFormValid ? "btn-disabled" : ""}`}
          >
            ➕ Submit Patient
          </button>
        </form>

        {successMessage && (
          <div className="success-text text-center">{successMessage}</div>
        )}
        {submitError && (
          <div className="error-text text-center">{submitError}</div>
        )}
      </div>
    </div>
  )
}

export default PatientForm
