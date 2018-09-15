import React, { Component } from "react";
import { Link } from "react-router-dom";

export default class Dashboard extends Component {
  render() {
    return (
      <div className="dashboard">
        <h1>Dashboard</h1>
        <div className="links">
          <ul>
            <li>
              <Link to="/job">JOB</Link>
            </li>
            <li>
              <Link to="/prefs">PREFERENCES</Link>
            </li>
            <li>
              <Link to="/city">CITY</Link>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}
