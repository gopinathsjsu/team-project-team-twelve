import * as React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import dayjs, { Dayjs } from 'dayjs';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import {DateTimePicker} from '@mui/x-date-pickers/DateTimePicker';
import moment from "moment"
import { RUD_FLIGHT_SCHEDULE as API, PATCH_API } from "../../RestAPI/Constants";

export default function UpdateFlightInfoForm({ isAdd, flightDetails, onChangeFlightDetails }) {
    const [value, setValue] = React.useState(dayjs('2022-04-07')); //this is my date
    const [firstTime, setFirstTime] = React.useState("firstTime");
    const [age, setAge] = React.useState('');

    const handleChange = (event) => {
        setAge(event.target.value);
    };


    const getDate = (date) => {
        if (!isAdd) {
            const d = moment(new Date(date)).format("YYYY-MM-DD");
        const t = moment(new Date(date)).format("HH:mm:ss");
            onChangeFlightDetails(t, 'time')
            onChangeFlightDetails(d, 'date')
        }
        else  {
            const d = moment(new Date(date)).format("YYYY-MM-DD HH:mm:ss");
            onChangeFlightDetails(d, 'time')
        }
    }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Add/Update Details
      </Typography>
      <Grid container spacing={3}>
      <Grid item xs={12}>
            <TextField
              required
              id="airline_flight_key"
              name="airline_flight_key"
              label="Airline flight key"
              fullWidth
              value={flightDetails.airline_flight_key}
              focused={flightDetails.airline_flight_key !== ""}
              autoComplete="given-name"
              variant="standard"
            />
          </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="source"
            name="source"
            label="Source"
            fullWidth
            value={flightDetails.source}
            onChange={(e) => onChangeFlightDetails(e.target.value, 'source')}
            focused={flightDetails.source !== ""}
            autoComplete="family-name"
            variant="standard"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="destination"
            name="destination"
            value={flightDetails.destination}
            onChange={(e) => onChangeFlightDetails(e.target.value, 'destination')}
            focused={flightDetails.destination !== ""}
            label="Destination"
            fullWidth
            autoComplete="shipping address-line1"
            variant="standard"
          />
        </Grid>
        <Grid item xs={4}>
            {/* <>DATE TIME SELECTOR</> */}
            <DateTimePicker
                label="Date&Time picker"
                default={new Date()}
                value={value}
                onChange={getDate}
                renderInput={(params) => <TextField {...params} />}
        />
        </Grid>
        <Grid item xs={4}>
        <TextField
            required
            id="baggagecarousel"
            name="baggagecarousel"
            label="Baggage Carousel"
            value={flightDetails.baggage_carousel}
            onChange={(e) => onChangeFlightDetails(e.target.value, 'source')}
            focused={flightDetails.baggage_carousel !== ""}
            fullWidth
            disabled={true}
            variant="standard"
          />
        </Grid>
        <Grid item xs={4}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Arrival/Departure</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={flightDetails.arrival_departure}
                    focused={flightDetails.arrival_departure !== ""}
                    label="ArrivalOrDeparture"
                    onChange={(e) => onChangeFlightDetails(e.target.value, 'arrival_departure')}
                >
                    <MenuItem value={"arrival"}>Arrival</MenuItem>
                    <MenuItem value={"departure"}>Departure</MenuItem>
                </Select>
            </FormControl>
        </Grid>
        <Grid item xs={12}>
          <TextField
            required
            id="remarks"
            name="remarks"
            label="Remarks"
            fullWidth
            value={flightDetails.remarks}
            onChange={(e) => onChangeFlightDetails(e.target.value, 'remarks')}
            variant="standard"
          />
        </Grid>
      </Grid>
    </React.Fragment>
    </LocalizationProvider>
  );
}

const doOnChange = () => {

}