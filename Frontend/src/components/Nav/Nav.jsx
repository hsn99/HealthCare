import React from "react"
import { Link } from "react-router-dom"
import "./Nav.css"

const Nav = ({ handleLogOut }) => {
  const userId = localStorage.getItem("userId")

  return (
    <nav className="navbar">
      <div>
        <Link to="/" aria-label="Home">
          Home
        </Link>
      </div>

      <div>
        {userId ? (
          <div>
            <Link onClick={handleLogOut} to="/" className="navButton">
              Sign Out
            </Link>
          </div>
        ) : (
          <div className="nav-section guest-user-links">
            <Link to="/login" className="navButton">
              Login
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Nav
