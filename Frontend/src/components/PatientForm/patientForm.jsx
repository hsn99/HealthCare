import React, { useState } from "react"
import axios from "axios"

const PatientForm = () => {
  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    weight: "",
    height: "",
    contact_info: "",
    // doctor_id: "",
    // room_id: "",
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
        age: parseInt(form.age),
        weight: parseFloat(form.weight),
        height: parseInt(form.height),
        // doctor_id: parseInt(form.doctor_id),
        // room_id: parseInt(form.room_id),
      }

      await axios.post("http://localhost:8000/patients", payload)
      setSuccessMessage("✅ Patient added successfully!")
      setForm({
        name: "",
        age: "",
        gender: "",
        weight: "",
        height: "",
        contact_info: "",
        // doctor_id: "",
        // room_id: "",
      })
      setFingerprintId(null)
    } catch (err) {
      console.error(err)
      setSubmitError("❌ Failed to create patient.")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-8 px-4">
      <div className="w-full max-w-2xl bg-white shadow-xl rounded-2xl p-8 space-y-6">
        <h2 className="text-3xl font-bold text-center text-gray-800">
          🩺 Add New Patient
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
            {/* <input
              type="number"
              name="doctor_id"
              placeholder="Doctor ID"
              value={form.doctor_id}
              onChange={handleChange}
              className="input-style"
            />
            <input
              type="number"
              name="room_id"
              placeholder="Room ID"
              value={form.room_id}
              onChange={handleChange}
              className="input-style"
            /> */}
          </div>

          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={handleScanFingerprint}
              disabled={isScanning}
              className={`px-5 py-2 rounded-lg text-white font-semibold ${
                isScanning
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {isScanning ? "Scanning..." : "🔍 Scan Fingerprint"}
            </button>
            {fingerprintId && (
              <span className="text-green-600 font-medium">
                ✅ Scanned: ID {fingerprintId}
              </span>
            )}
            {scanError && (
              <span className="text-red-600 font-medium">{scanError}</span>
            )}
          </div>

          <button
            type="submit"
            className={`w-full py-3 text-lg rounded-lg font-bold text-white transition ${
              fingerprintId
                ? "bg-green-600 hover:bg-green-700"
                : "bg-gray-400 cursor-not-allowed"
            }`}
          >
            ➕ Submit Patient
          </button>
        </form>

        {/* Feedback Messages */}
        {successMessage && (
          <div className="text-center text-green-700 font-semibold">
            {successMessage}
          </div>
        )}
        {submitError && (
          <div className="text-center text-red-600 font-semibold">
            {submitError}
          </div>
        )}
      </div>

      {/* Tailwind input styling override */}
      <style>{`
        .input-style {
          @apply w-full px-4 py-2 border rounded-lg border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400;
        }
      `}</style>
    </div>
  )
}

export default PatientForm
