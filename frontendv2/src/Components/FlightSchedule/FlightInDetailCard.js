import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { Avatar, Button, CardActionArea } from '@mui/material';
import ArrowForwardSharpIcon from '@mui/icons-material/ArrowForwardSharp';
import EventIcon from '@mui/icons-material/Event';

// Quick View

const getBaggageOrRemarks = (flight) => {
  if (flight.arrival_departure === "departure") {
    return (
      <Button variant="contained"  sx={{ alignProperty: "center", ml: 2, mr: 2, display: "flex", flexDirection: "column"}}> 
          <Typography variant="overline" sx={{fontSize: 8}}>Remark</Typography>
          <Typography variant="h5" sx={{fontSize: 16}}>{flight.remarks}</Typography>
      </Button>
    )
  } else if (flight.arrival_departure === "arrival") {
    return (
      <Button variant="contained" sx={{ alignProperty: "center", ml: 2, mr: 2, display: "flex", flexDirection: "column"}}> 
        <Typography variant="overline" sx={{fontSize: 8}}>#Bagg.</Typography>
        <Typography variant="h6">E1</Typography>
      </Button>
    )
  }
}

export default function FlightInDetailCard({ flight }) {
  return (
      <Box sx={{display: 'flex', alignItems: "center", justifyContent: "center"}}>
        <Card sx= {{ width: 0.75, p: 1, display: 'flex-inline', flexDirection: 'row', alignItems: "center", justifyContent: "center"}}>
          <Box sx={{ display: "flex", flexDirection: "row" , alignItems: "center", justifyContent: "center"}}>

          <Button variant="contained" sx={{ alignProperty: "center", ml: 2, mr: 2, display: "flex", flexDirection: "column"}}> 
                <Typography variant="overline" sx={{fontSize: 8, color: "white"}}>#Gate</Typography>
                <Typography variant="h6">A1</Typography>
          </Button>

            <Typography variant="h6" sx={{mr: 4}} >{flight.airline_flight_key}</Typography>
            
            <Box sx={{ mr: 4, display: 'flex', flexDirection: 'column', alignItems: "center"}}>
              <Typography variant="h5">SJC</Typography>
              <Typography variant="body2">({flight.source})</Typography>  
            </Box>

            <ArrowForwardSharpIcon sx={{ fontSize: 30, alignSelf: "center"}} />

            <Box sx={{ ml: 4, display: 'flex', flexDirection: 'column', alignItems: "center"}}>
              <Typography variant="h5">DAL</Typography>
              <Typography variant="body2">({flight.destination})</Typography>  
            </Box>

            <Box sx={{ ml: 4, display: 'flex', flexDirection: 'row', alignItems: "center"}}>
              <Typography variant="body1" sx={{ fontSize:15 , mr: 1}}>{flight.time}</Typography> /
              <Typography variant="body1" sx={{ fontSize:15 , ml: 1}}>({flight.date})</Typography>  
            </Box>

            {getBaggageOrRemarks(flight)}

          </Box>
        </Card>
      </Box>
  );
}
