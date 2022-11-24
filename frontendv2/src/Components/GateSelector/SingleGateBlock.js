import * as React from "react";
import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography";

export default function SingleGateBlock({ active, gateCode }){
    return (
        <Box sx={{
        height: 100,
        width: 100,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: active ? "green" : "#fff",
        margin: 1,
        shadow: 4,
        textAlign: "center",
        color: active ? "white" : "black",
        cursor: "pointer", "&:hover": {
          color: "white",
          backgroundColor: "green",
        },
          }}>
            <Typography variant="h5">{gateCode}</Typography>
        </Box>
    );
}