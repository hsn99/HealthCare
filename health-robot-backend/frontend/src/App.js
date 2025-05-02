import React, { useState } from 'react';

function App() {
  const [patientData, setPatientData] = useState({
    patient_id: '',
    temperature: '',
    weight: '',
    blood_pressure: '',
    pulse: ''
  });

  // Handle input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPatientData({ ...patientData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/submit-readings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData),  // Send form data as JSON
      });

      const result = await response.json();
      alert(`Response: ${result.status}`);
    } catch (error) {
      console.error('Error submitting readings:', error);
    }
  };

  return (
    <div className="App">
      <h1>Healthcare Robot Dashboard</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Patient ID:
          <input
            type="text"
            name="patient_id"
            value={patientData.patient_id}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <label>
          Temperature:
          <input
            type="number"
            name="temperature"
            value={patientData.temperature}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <label>
          Weight:
          <input
            type="number"
            name="weight"
            value={patientData.weight}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <label>
          Blood Pressure:
          <input
            type="text"
            name="blood_pressure"
            value={patientData.blood_pressure}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <label>
          Pulse:
          <input
            type="number"
            name="pulse"
            value={patientData.pulse}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <button type="submit">Submit Readings</button>
      </form>
    </div>
  );
}

export default App;
