import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import dayjs, { Dayjs } from 'dayjs';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';
import { Typography } from '@mui/material';

export default function SelectFlightCard({ myAirlines = [], selectedFlight, setSelectedFlight, value, setValue }) {

  const handleChange = (newValue) => {
    setValue(newValue);
  };
  // const [selectedFlight, setSelectedFlight] = React.useState(selected);
  console.log('------myAirlines------', myAirlines)

  if (myAirlines.length === 0) return <></>;

  var selected = myAirlines[0].airline_flight_key;

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <FormControl>
        <FormLabel id="demo-radio-buttons-group-label">
          <Typography variant="h5">Available Flights for</Typography>
          <DesktopDatePicker
            label=""
            inputFormat="MM/DD/YYYY"
            value={value}
            onChange={handleChange}
            renderInput={(params) => <TextField {...params} />}
          />
        </FormLabel>
          
        <RadioGroup
          aria-labelledby="demo-radio-buttons-group-label"
          value={selectedFlight}
          name="radio-buttons-group"
          onChange={(event)=>{setSelectedFlight(event.target.value)}}
        >
          {myAirlines.map((flight) => (
            <FormControlLabel key={flight.airline_flight_key} value={flight.airline_flight_key} control={<Radio />} label={getLabel(flight)} />
          ))}
        </RadioGroup>
      </FormControl>
    </LocalizationProvider>
  );
}

const getLabel = (flight) => {
  let label = flight.airline_name + " " + flight.airline_flight_key;
  return label;
}

