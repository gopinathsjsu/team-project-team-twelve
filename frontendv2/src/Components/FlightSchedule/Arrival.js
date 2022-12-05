import * as React from "react";
import { experimentalStyled as styled } from '@mui/material/styles';
import { Stack, Typography } from "@mui/material";
import {FLIGHT_SCHEDULE_LIST_API as API} from '../../RestAPI/Constants';
import LinearProgress from '@mui/material/LinearProgress';
import FlightCard from "./FlightCard";
import Box from '@mui/material/Box';
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Avatar from "@mui/material/Avatar"
import FlightInDetailCard from "./FlightInDetailCard";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import { alignProperty } from "@mui/material/styles/cssUtils";
import Select, { SelectChangeEvent } from '@mui/material/Select'

class Arrival extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: [],
            isLoaded: false,
            screen: props.screen,
            terminal: "T1",
            hours: "1"
        }
    }

    componentDidMount(timeSlot = "1") {
        this.hitFlightScheduleAPI(timeSlot);
    }

    hitFlightScheduleAPI(timeSlot = "1") {
        console.log(timeSlot)
        var date = new Date();
        var timeGTE = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
        var timeLTE = (date.getHours() + Number(timeSlot)) + ":" + date.getMinutes() + ":" + date.getSeconds();
        var dateGTE = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
        var dateLTE = dateGTE;

        var queryParams = {
            "time__gte": timeGTE,
            "time__lte": timeLTE,
            "date__gte": dateGTE,
            "date__lte": dateLTE
        }
        var url = new URL(API);
        Object.keys(queryParams).forEach(key => url.searchParams.append(key, queryParams[key]));

        var debugurl = "https://60261217186b4a001777fbd7.mockapi.io/api/ndkshr/flight-schedule-list";

        fetch(url)
        .then(res => res.json())
        .then(json => {
            this.setState({
                items: json,
                isLoaded: true,
                screen: this.state.screen,
                terminal: "T1",
                hours: timeSlot,
            })
        });
    }

    render() {
        var { items, isLoaded, screen, terminal, hours } = this.state;
    
        if (!isLoaded) {
            return (
                <LinearProgress color="secondary" />
            )
        } else {
            return (
                <div>
                    <Grid sx={{justifyContent: "center", display: "flex"}}>
                        <FormControl sx={{m: 2, minWidth: 120}}>
                            <InputLabel id="select-terminal">Terminal</InputLabel>
                            <Select
                                value={terminal}
                                label="Terminal"
                                onChange={(event) => this.handleTerminalChange(event)}
                            >
                                <MenuItem value={"T1"}>Terminal 1</MenuItem>
                                <MenuItem value={"T2"}>Terminal 2</MenuItem>
                                <MenuItem value={"T3"}>Terminal 3</MenuItem>
                            </Select>
                        </FormControl>
                        <FormControl sx={{m: 2, minWidth: 120}}>
                            <InputLabel id="select-time-slot">Hours</InputLabel>
                            <Select
                                value={hours}
                                label="Hours"
                                onChange={(event) => this.handleHourChange(event)}
                            >
                                <MenuItem value={"1"}>1 hr</MenuItem>
                                <MenuItem value={"2"}>2 hrs</MenuItem>
                                <MenuItem value={"4"}>4 hrs</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Stack sx={{ p: 2}} spacing={2}>
                        {this.getItemsAfterFilter(screen, items).map((item, idx) => (
                            this.getCard(screen, item)
                        ))}
                    </Stack>
                </div>
            );
        }
    }

    handleTerminalChange(terminal) {
        this.setState({terminal: terminal.target.value})
    }

    handleHourChange(timeSlotEvent) {
        this.setState({hours: timeSlotEvent.target.value})
        this.componentDidMount(timeSlotEvent.target.value);
    }

    getItemsAfterFilter(screen, items) {
        let currentTerminal = this.state.terminal;
        
        if (screen === "dashboard") return (
            items.filter(item => item.arrival_departure === "arrival" && null !== item.terminal_gate_key && item.terminal_gate_key.includes(currentTerminal)).slice(0, 5)
        );
        else  return (
            items.filter(item => item.arrival_departure === "arrival" && null !== item.terminal_gate_key && item.terminal_gate_key.includes(currentTerminal))
        );
    }
    
    getCard(screen, item) {
        if (screen === "dashboard") {
            return <FlightCard flight={item}/> 
        } else {
            return <FlightInDetailCard flight={item}/>
        }
    }
}

export default Arrival;
