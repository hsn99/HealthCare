import { useState } from "react"
import axios from "axios"
import "./doctorForm.css"

const DoctorForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    specialization: "",
    room_id: "",
  })

  const [message, setMessage] = useState({ type: "", text: "" })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await axios.post("http://localhost:8000/doctors/", {
        name: formData.name,
        specialization: formData.specialization,
        room_id: parseInt(formData.room_id),
      })

      setMessage({
        type: "success",
        text: `Doctor ${response.data.name} added successfully!`,
      })
      setFormData({ name: "", specialization: "", room_id: "" })
    } catch (error) {
      console.error(error)
      setMessage({ type: "error", text: "Error: Could not add doctor." })
    }
  }

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="form-box">
        <h2 className="form-title">Add New Doctor</h2>

        <div className="form-grid">
          <div className="form-fields">
            <input
              type="text"
              name="name"
              placeholder="Doctor Name"
              value={formData.name}
              onChange={handleChange}
              className="input-style"
              required
            />
            <input
              type="text"
              name="specialization"
              placeholder="Specialization"
              value={formData.specialization}
              onChange={handleChange}
              className="input-style"
              required
            />
            <input
              type="number"
              name="room_id"
              placeholder="Room ID"
              value={formData.room_id}
              onChange={handleChange}
              className="input-style"
              required
            />
          </div>
          <button type="submit" className="submit-btn">
            Add Doctor
          </button>
        </div>

        {message.text && (
          <p
            className={`text-center ${
              message.type === "success" ? "success-text" : "error-text"
            }`}
          >
            {message.text}
          </p>
        )}
      </form>
    </div>
  )
}

export default DoctorForm
