// Nav.jsx
import React from "react"
import { Link } from "react-router-dom"
import "./Nav.css"
import logo from "./logo.png"

const Nav = ({ user, handleLogOut }) => {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="logo-link">
          <img src={logo} alt="ON POWER Logo" className="logo" />
        </Link>
      </div>
      <div className="navbar-right">
        {user ? (
          <>
            <span className="nav-username">Hello, {user.name}</span>
            <button onClick={handleLogOut} className="navButton">
              Sign Out
            </button>
          </>
        ) : (
          <div className="navbar-right">
            <Link to="/admin-panel" className="navButton">
              <span>Admin Panel</span>
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Nav
