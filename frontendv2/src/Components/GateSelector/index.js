import React, { useEffect, useState } from "react";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import { experimentalStyled as styled, withTheme } from "@mui/material/styles";
import BlockIcon from '@mui/icons-material/Block';
import { Typography } from "@mui/material";
import {GATE_LIST as API, PATCH_GATE_STATUS} from "../../RestAPI/Constants";
import {PATCH_GATE_STATUS as CHANGE_STATUS_API} from "../../RestAPI/Constants";
import { WindowSharp } from "@mui/icons-material";

const Item = styled("div")(({ theme, colorCodes }) => ({
  height: 100,
  width: 100,
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  backgroundColor: colorCodes.backgroundColor,
  margin: 8,
  textAlign: "center",
  color: colorCodes.color,
  borderRadius: 25,
  cursor: "pointer", "&:hover": {
    color: "white",
    backgroundColor: theme.palette.primary.main,
  },
}));

const GateSelector = () => {
  const [activeTerminal, setActiveTerminal] = useState("T1");
  const [selectedGate, setSelectedGate] = useState(null);
  const [gateData, setGateData] = useState([]);
  const [selectedGateState, setSelectedGateState] = useState("open");

  useEffect(() => {
    fetchTerminalGates();
  }, [activeTerminal]);

  const fetchTerminalGates = () => {
    fetch(API)
    .then(res => res.json())
    .then(gates => {
      setGateData(gates);
    });
  } 

  const onSelectGate = (gate, gateState) => {
    setSelectedGate(gate);
    setSelectedGateState(gateState);
  };

  const patchGateStatus = (gate_status) => {
    let patchUrl = PATCH_GATE_STATUS + selectedGate + "/"; 
    let token = "Bearer " + window.sessionStorage.getItem("access_token");
    
    let requestBody = JSON.stringify({
      "gate_status": gate_status
    });
    fetch(patchUrl, {
      method: "PATCH",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": token
      },
      body: requestBody
    }).then(res => res.json())
    .then(json => {
      if (json.gate_status === gate_status && json.terminal_gate === selectedGate) {
        setSelectedGate(null);
        setSelectedGateState("open");
        fetchTerminalGates();
      }
    })
  }

  const onBlockGate = () => {
    patchGateStatus("maintain");
  };

  const onOpenGate = () => {
    patchGateStatus("open");
  };

  const onGateClick = () => {
  
    let gate_status = gateData.find(gate => gate.terminal_gate == selectedGate).gate_status;
    if (gate_status == "maintain") {
      onOpenGate();
    } else if (gate_status === "open") {
      onBlockGate();
    }
  }

  const renderTerminals = () => {
    return (
      <Container
        maxWidth="sm"
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginTop: "16px",
          marginBottom: "16px",
        }}
      >
        <Button
          variant="contained"
          size="large"
          onClick={() => setActiveTerminal("T1")}
        >
          Terminal 1
        </Button>
        <Button
          variant="contained"
          size="large"
          onClick={() => setActiveTerminal("T2")}
        >
          Terminal 2
        </Button>
        <Button
          variant="contained"
          size="large"
          onClick={() => setActiveTerminal("T3")}
        >
          Terminal 3
        </Button>
      </Container>
    );
  };

  const renderGateGrid = (gateList) => {
    var gatesForTerminal = []
    if (gateList !== undefined){
      gatesForTerminal = gateList.filter((gate) => null !== gate.terminal_gate && gate.terminal_gate.includes(activeTerminal))
      
      gatesForTerminal.sort(
        (a, b) => {
          return parseInt(a.terminal_gate.split("_")[1].substring(1)) - parseInt(b.terminal_gate.split("_")[1].substring(1))
        }
      );
      
    }
      
    return (
      <Grid container columns={{ xs: 8, sm: 8, md: 8 }} sx={{p: 2}}>
        {gatesForTerminal.map((gate, _) => (
          <Grid item xs={1} sm={1} md={1} key={gate.terminal_gate}>
            <Item
              colorCodes={selectedGate === gate.terminal_gate ? status_map.selected : status_map[gate.gate_status]}
              onClick={() => onSelectGate(gate.terminal_gate, gate.gate_status)}
            >
              <Typography variant="h5">{gate.terminal_gate.split("_")[1]}</Typography>
            </Item>
          </Grid>
        ))}
      </Grid>
    );
  };

  const status_map = {
    open: {backgroundColor: "white", color: "black"},
    maintain: {backgroundColor: "yellow", color: "black"},
    close: {backgroundColor: "red", color: "white"},
    selected: {backgroundColor: "#1976d2", color: "white"}
  }

  const button_map = {
    open: {color: "error", text: "Close Gate"},
    maintain: {color: "success", text: "Open Gate"},
    close: {color: "success", text: "Open Gate"}
  }

  const renderActionBtns = () => {
    let buttonColor = button_map[selectedGateState].color;
    let buttonText = button_map[selectedGateState].text;
    console.log("myasdf", selectedGateState);
    return (
      <Container maxWidth="xs" sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        marginTop: "16px",
        marginBottom: "16px",
      }} columns={{xs: 12, sm: 12, md: 12}}>
        <Button variant="contained" color={buttonColor} size="large" onClick={onGateClick} startIcon={<BlockIcon />}>
          {buttonText}
        </Button>
      </Container>
    );
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {renderTerminals()}
      {renderGateGrid(gateData)}
      {renderActionBtns()}
    </Box>
  );
};

export default GateSelector;
