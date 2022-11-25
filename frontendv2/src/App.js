import * as React from "react";
import FlightCard from "./Components/FlightSchedule/FlightCard";
import Arrival from "./Components/FlightSchedule/Arrival";
import Login from "./Components/Login/Login";
import Dashboard from "./Components/Dashboard/Dashboard";
import GateSelector from "./Components/GateSelector";

function App() {
  return (
    <div>
      {/* <Arrival></Arrival> */}
      {/* <Login></Login> */}
      <Dashboard></Dashboard>
      {/* <GateSelector /> */}
    </div>
  );
}

export default App;
