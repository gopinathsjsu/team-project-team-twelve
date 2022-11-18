import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { CardActionArea } from '@mui/material';
import ArrowForwardSharpIcon from '@mui/icons-material/ArrowForwardSharp';
import EventIcon from '@mui/icons-material/Event';

// Quick View
export default function FlightCard({ flight }) {
  return (
    <div>
      <Box sx={{felxGrow: 1}}>
        <Card sx= {{ width: 1, p: 1, display: 'flex', flexDirection: 'row' , alignItems: 'center', justifyContent: "center"}}>
          <Box sx={{ display: "flex", flexDirection: "row" , alignItems: "center"}}>

            <Typography variant="subtitle1" sx={{mr: 4}} >{flight.airline_flight_key}</Typography>
            
            <Box sx={{ mr: 4, display: 'flex', flexDirection: 'column', alignItems: "center"}}>
              <Typography variant="h5">SJC</Typography>
              <Typography variant="body2">({flight.source})</Typography>  
            </Box>

            <ArrowForwardSharpIcon sx={{ fontSize: 30 }} />

            <Box sx={{ ml: 4, display: 'flex', flexDirection: 'column', alignItems: "center"}}>
              <Typography variant="h5">DAL</Typography>
              <Typography variant="body2">({flight.destination})</Typography>  
            </Box>

            <Box sx={{ ml: 4, display: 'flex', flexDirection: 'column', alignItems: "center"}}>
              <Typography variant="body1" sx={{ fontSize:12 }}>{flight.time}</Typography>
              <Typography variant="body1" sx={{ fontSize:12 }}>({flight.date})</Typography>  
            </Box>

          </Box>
        </Card>
      </Box>
    </div>
  );
}
