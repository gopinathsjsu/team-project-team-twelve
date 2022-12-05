import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { Stack, Typography } from "@mui/material";
import Button from '@mui/material/Button';
import Title from './Title';
import Arrival from '../FlightSchedule/Arrival';
import Departure from '../FlightSchedule/Departure';

function preventDefault(event) {
  event.preventDefault();
}

export default function DashboardFlightScheduleCard({ heading, selected, setSelected }) {
  let key = heading.toLowerCase();
  console.log("heading key", key);
  return (
    <React.Fragment>
      {/* <Title>{ heading }</Title> */}
      <Typography variant="h4" color="primary.main">{heading}</Typography>
      {getArrivalDepartureView(heading)}
      <Link color="primary" href="#" onClick={preventDefault} sx={{ mt: 1 }}>
        <Button variant="contained" onClick={(e) => setSelected({key})} selected={selected == key}> View All </Button>
      </Link>
    </React.Fragment>
  );
}

const getArrivalDepartureView = (heading) => {
  if (heading === "Departures") {
    return (
      <Departure screen="dashboard" />
    )
  } else if (heading === "Arrivals") {
    return (
      <Arrival screen="dashboard" />
    )
  }
}