import "./homepage.css"
import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"

const Home = () => {
  const [user, setUser] = useState(null)
  const [checking, setChecking] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const interval = setInterval(async () => {
      setChecking(true)
      try {
        const response = await axios.get(
          "http://localhost:8000/auth/fingerprint/last"
        )
        if (response.data.status === "success") {
          setUser(response.data.user)
          localStorage.setItem("user_id", response.data.user.id)
          setChecking(false)
          navigate("/test")
        }
      } catch (err) {
        console.error("Error checking fingerprint:", err)
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      {user ? (
        <div>
          <h2>Welcome, {user.name}!</h2>
        </div>
      ) : (
        <div>
          <h3>Waiting for fingerprint scan...</h3>
          {checking && <p>Checking...</p>}
        </div>
      )}
    </div>
  )
}

export default Home
