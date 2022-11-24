import React, { useEffect, useState } from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import Paper from '@mui/material/Paper';
import Stepper from '@mui/material/Stepper';
import dayjs, { Dayjs } from 'dayjs';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import AddFlightInfoForm from './AddFlightInfoForm'; 
import AddIcon from '@mui/icons-material/Add';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import SaveIcon from '@mui/icons-material/Save';
import SelectFlightCard from './SelectFlightCard'
import {AIRLINE_LIST as API, PATCH_API as ADD_UPDATE_FLIGHT, CREATE_FLIGHT} from "../../RestAPI/Constants";

export default function AirlineManagementPage() {

  const [date, setDate] = React.useState(
    dayjs('2014-08-18'),
  );
  const [isAdd, setIsAdd] = React.useState(false);
  const [activeStep, setActiveStep] = React.useState(0);
  const [myFlights, setMyFlights] = React.useState([]);
  const [selectedFlight, setSelectedFlight] = React.useState("");
  const [flightDetails, setFlightDetails] = React.useState({
    "fact_guid": "",
    "airline_flight_key": "",
    "source": "",
    "destination": "",
    "arrival_departure": "",
    "date": "",
    "time": "",
    "terminal_gate_key": "",
    "gate_close_time": "",
    "gate_open_time": "",
    "baggage_carousel": "",
    "remarks": ""
});

useEffect(() => {
      if (activeStep === 1 && !isAdd) {
        fetchFlightDetails();
      }
  },[activeStep])

  React.useEffect(
    () => {
      console.log("i choose you ", selectedFlight);
    },
    [selectedFlight]
  )

  const steps = ['Select Flight', 'Add/Update Details'];

  React.useEffect(
    () => {
      fetchMyAirlines();
    },
    []
  );

  const fetchMyAirlines = () => {
    let fetchUrl = API;
    let token = "Bearer " + window.sessionStorage.getItem("access_token");
    const response = fetch (fetchUrl, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": token
      },
    }).then(response => response.json())
    .then(json => {
      setMyFlights(json);
    })
  }

  const getInTwoDigits = (num) => {
    if (num < 10) {
        return "0"+num;
    } else {
        return num;
    }
}

const onChangeFlight = (flight) => {
  setSelectedFlight(flight);
  setFlightDetails({
    ...flightDetails,
    airline_flight_key: flight
  })
}

  const fetchFlightDetails = () => {
    var dateObj = new Date(date)
    let formattedDate = dateObj.getFullYear() + "_" + getInTwoDigits(dateObj.getMonth() + 1) + "_" + getInTwoDigits(dateObj.getDate());
    let flightKey = selectedFlight + "_" + formattedDate; // dont forget to format the date
    let fetchUrl = ADD_UPDATE_FLIGHT + flightKey;
    console.log("flightkey", flightKey);
    let token = "Bearer " + window.sessionStorage.getItem("access_token");
    fetch (fetchUrl, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "Authorization": token
        },
        
    }).then(response => response.json())
    .then(json => {
        setFlightDetails(json);
    })
}

const onUpdateFlight = () => {
  var dateObj = new Date(date)
  let formattedDate = dateObj.getFullYear() + "_" + getInTwoDigits(dateObj.getMonth() + 1) + "_" + getInTwoDigits(dateObj.getDate());
  let url = ADD_UPDATE_FLIGHT + selectedFlight + "_" + formattedDate;
  let token = "Bearer " + window.sessionStorage.getItem("access_token");
  fetch (
    url,
    {
        method: "PUT",
        body: JSON.stringify(flightDetails),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          "Authorization": token
        }
    }
).then(res => res.json())
.then(json => {
    console.log('---------flight details submit--------', json)
})
}

const onAddFlight = () => {
  var dateObj = new Date(date)
  let formattedDate = dateObj.getFullYear() + "_" + getInTwoDigits(dateObj.getMonth() + 1) + "_" + getInTwoDigits(dateObj.getDate());
  let url = CREATE_FLIGHT + selectedFlight + "_" + formattedDate;
  let token = "Bearer " + window.sessionStorage.getItem("access_token");
  fetch (
    url,
    {
        method: "POST",
        body: JSON.stringify(flightDetails),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          "Authorization": token
        }
    }
).then(res => res.json())
.then(json => {
    console.log('---------flight details submit--------', json)
})
}

const onSubmitFlightDetails = () => {
  if (isAdd) {
    onAddFlight();
  } else {
    onUpdateFlight();
  }
}
  
  function getStepContent(step) {
    switch (step) {
      case 0:
        return <SelectFlightCard myAirlines={myFlights} selectedFlight = {selectedFlight} setSelectedFlight={onChangeFlight} 
          value={date} setValue={setDate}
        />;
      case 1:
          return <AddFlightInfoForm isAdd = {isAdd} flightDetails={flightDetails} onChangeFlightDetails={onChangeFlightDetails} />
      default:
        throw new Error('Unknown step');
    }
  }
  
  const theme = createTheme();

  const handleNext = () => {
    // if (selectedFlight === "") return;
    setActiveStep(activeStep + 1);

    if (activeStep === 1) {
      onSubmitFlightDetails();
    }
  };

  const handleBack = () => {
    setIsAdd(false);
    setActiveStep(activeStep - 1);
  };

  const handleAddNew = () => {
    setIsAdd(true);
    handleNext();
  }

  const goToStep = (stepNo) => {
    setActiveStep(stepNo);
  }

  const onChangeFlightDetails = (value, field) => setFlightDetails({
    ...flightDetails,
   [field]: value
});

  // fetchMyAirlines();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container component="main" maxWidth="md" sx={{ mb: 4 }}>
        <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
          <Typography variant="h4" align="center" color="primary.main">
            Airline Management
          </Typography>
          <Stepper activeStep={activeStep} sx={{ pt: 3, pb: 5 }}>
            {steps.map((label, idx) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
          {activeStep === steps.length ? (
            <React.Fragment>
              <Typography variant="h5" gutterBottom>
                Flight Update Success
              </Typography>
              <Typography variant="subtitle1">
                {/* Flight {flightkey} was updated */}
              </Typography>
            </React.Fragment>
          ) : (
            <React.Fragment>
              {getStepContent(activeStep, false)}

              <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                {activeStep !== 0 && (
                  <Button variant="outlined" onClick={handleBack} sx={{ mt: 3, ml: 1 }} startIcon={<ChevronLeftIcon />}>
                    Back
                  </Button>
                )}

                {activeStep === 0 && (
                    <Button variant="outlined" onClick={handleAddNew} sx={{ mt: 3, ml: 1 }}>
                      Add New
                    </Button>
                  )}

                <Button
                  variant="contained"
                  onClick={handleNext}
                  sx={{ mt: 3, ml: 1 }}
                  endIcon={activeStep === steps.length - 1 ? <SaveIcon /> : <NavigateNextIcon />}
                >
                  {activeStep === steps.length - 1 ? 'Save' : 'Next'}
                </Button>
              </Box>
            </React.Fragment>
          )}
        </Paper>
      </Container>
    </ThemeProvider>
  );
}