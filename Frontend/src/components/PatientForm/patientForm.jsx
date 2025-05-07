import React, { useState } from "react"
import axios from "axios"
import "./PatientForm.css" // Import the CSS file

const PatientForm = () => {
  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    weight: "",
    height: "",
    contact_info: "",
  })

  const [fingerprintId, setFingerprintId] = useState(null)
  const [isScanning, setIsScanning] = useState(false)
  const [scanError, setScanError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")
  const [submitError, setSubmitError] = useState("")

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleScanFingerprint = async () => {
    setIsScanning(true)
    setScanError("")
    setSuccessMessage("")

    try {
      const res = await axios.post("http://localhost:8000/patients/enroll")
      setFingerprintId(res.data.fingerprint_id)
    } catch (err) {
      console.error(err)
      setScanError("❌ Fingerprint scanning failed.")
    } finally {
      setIsScanning(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitError("")
    setSuccessMessage("")

    try {
      const payload = {
        ...form,
        fingerprint_id: fingerprintId,
        age: Number(form.age) || 0,
        weight: parseFloat(form.weight) || 0,
        height: Number(form.height) || 0,
      }

      await axios.post("http://localhost:8000/patients", payload)

      setSuccessMessage("✅ Patient added successfully!")

      setTimeout(() => {
        setForm({
          name: "",
          age: "",
          gender: "",
          weight: "",
          height: "",
          contact_info: "",
        })
        setFingerprintId(null)
      }, 2000)
    } catch (err) {
      console.error(err)
      setSubmitError("❌ Failed to create patient.")
    }
  }

  const isFormValid =
    form.name && form.age && form.gender && fingerprintId

  return (
    <div className="form-container">
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
            <input
              type="number"
              step="0.01"
              name="weight"
              placeholder="Weight (kg)"
              value={form.weight}
              onChange={handleChange}
              className="input-style"
            />
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
              disabled={
                isScanning || !(form.name && form.age && form.gender)
              }
              className={`scan-btn ${
                isScanning || !(form.name && form.age && form.gender)
                  ? "btn-disabled"
                  : ""
              }`}
            >
              {isScanning ? "Scanning..." : "🔍 Scan Fingerprint"}
            </button>

            {fingerprintId && (
              <span className="success-text">
                ✅ Scanned: ID {fingerprintId}
              </span>
            )}
            {scanError && (
              <span className="error-text">{scanError}</span>
            )}
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
