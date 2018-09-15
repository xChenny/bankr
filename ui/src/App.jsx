// libraries
import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";

// styles
import "./styles/App.css";

// views
import ErrorPage from "./views/Error";
import HomePage from "./views/Home";
import DashboardPage from "./views/Dash";
import CityPage from "./views/City";
import JobPage from "./views/Job";
import PrefsPage from "./views/Prefs";

const App = () => (
  <Router>
    <div className="App">
      <Route exact path="/" component={HomePage} />
      <Route path="/error" component={ErrorPage} />
      <Route path="/dashboard" component={DashboardPage} />
      <Route path="/city" component={CityPage} />
      <Route path="/job" component={JobPage} />
      <Route path="/prefs" component={PrefsPage} />
    </div>
  </Router>
);

export default App;
