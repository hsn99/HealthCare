// homepage.jsx
import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import "./homepage.css"
import logo from "./logo.png"

const Home = ({ setUser }) => {
  const [checking, setChecking] = useState(false)
  const [localUser, setLocalUser] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const interval = setInterval(async () => {
      setChecking(true)
      try {
        const response = await axios.post(
          "http://localhost:8000/login/fingerprint"
        )
        if (response.data.status === "success") {
          const user = response.data.user
          setLocalUser(user)
          setUser(user)
          localStorage.setItem("user_id", user.id)
          localStorage.setItem("user_name", user.name)
          navigate("/test")
        }
      } catch (err) {
        console.error("Error checking fingerprint:", err)
      } finally {
        setChecking(false)
      }
    }, 3000)

    return () => clearInterval(interval)
  }, [navigate, setUser])

  return (
    <div className="homepage-container">
      <img src={logo} alt="ON POWER Logo" className="logo" />
      <div className="card">
        {!localUser ? (
          <>
            <h2 className="title">Welcome to the Health Assistant</h2>
            <p className="subtitle">Please scan your fingerprint to begin</p>
            <div className={`fingerprint ${checking ? "scanning" : ""}`}></div>
            {checking && <p className="status-text">Checking...</p>}
          </>
        ) : (
          <>
            <h2 className="title">Hello, {localUser.name}!</h2>
            <p className="subtitle">Redirecting to diagnostics...</p>
          </>
        )}
      </div>
      <footer className="footer">© 2025 ON POWER | All rights reserved</footer>
    </div>
  )
}

export default Home
