import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AssignmentIcon from '@mui/icons-material/Assignment';
import FlightLandOutlinedIcon from '@mui/icons-material/FlightLandOutlined';
import FlightTakeoffOutlinedIcon from '@mui/icons-material/FlightTakeoffOutlined';
import CelebrationOutlinedIcon from '@mui/icons-material/CelebrationOutlined';
import LoginIcon from '@mui/icons-material/Login';
import AirplaneTicketIcon from '@mui/icons-material/AirplaneTicket';
import LogoutIcon from '@mui/icons-material/Logout';

export default function AirlineEmployeeListItems({selected, setSelected}) {
  return (
    <React.Fragment>
      <ListItemButton onClick={(e) => setSelected("dashboard")} selected={selected == "dashboard"}>
        <ListItemIcon>
          <DashboardIcon sx={{ color: 'primary.main' }}/>
        </ListItemIcon>
        <ListItemText primary="Dashboard" />
      </ListItemButton>
      <ListItemButton onClick={(e) => setSelected("arrivals")} selected={selected == "arrival"}>
        <ListItemIcon>
          <FlightLandOutlinedIcon sx={{ color: 'green' }}/>
        </ListItemIcon>
        <ListItemText primary="Arrivals" />
      </ListItemButton>
      <ListItemButton onClick={(e) => setSelected("departures")} selected={selected == "departures"}>
        <ListItemIcon>
          <FlightTakeoffOutlinedIcon sx={{ color: 'red' }}/>
        </ListItemIcon>
        <ListItemText primary="Departures" />
      </ListItemButton>
      {/* <ListItemButton onClick={(e) => setSelected("login")} selected={selected == "login"}>
        <ListItemIcon>
          <LoginIcon sx={{ color: 'purple' }} />
        </ListItemIcon>
        <ListItemText primary="Log In" />
      </ListItemButton> */}
      <ListItemButton onClick={(e) => setSelected("airlineManagement")} selected={selected == "airlineManagement"}>
        <ListItemIcon>
          <AirplaneTicketIcon sx={{ color: 'purple' }} />
        </ListItemIcon>
        <ListItemText primary="Airline Management" />
      </ListItemButton>
      <ListItemButton onClick={(e) => setSelected("aboutus")} selected={selected == "aboutus"}>
        <ListItemIcon>
          <CelebrationOutlinedIcon sx={{ color: 'orange' }} />
        </ListItemIcon>
        <ListItemText primary="About Us" />
      </ListItemButton>
      <ListItemButton onClick={(e) => setSelected("logout")} selected={selected == "logout"}>
        <ListItemIcon>
          <LogoutIcon sx={{ color: 'grey' }} />
        </ListItemIcon>
        <ListItemText primary="Log Out" />
      </ListItemButton>
    </React.Fragment>
  );
}