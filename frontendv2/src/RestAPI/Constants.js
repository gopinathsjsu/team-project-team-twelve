// http://ec2-3-141-169-170.us-east-2.compute.amazonaws.com:8000/auth_urls/flight-schedule-list

export const SCHEME = "http://";
export const DOMAIN = "ec2-18-116-238-148.us-east-2.compute.amazonaws.com";
export const PORT = ":8000";
export const API_PATH = "/auth_urls"

// AMS_API Domain URL
export const AMS_API = SCHEME + DOMAIN + PORT + API_PATH;

// API Endpoint URLs path suffix
export const FLIGHT_SCHEDULE_LIST_API = AMS_API + "/flight-schedule-list";
// http://ec2-3-141-169-170.us-east-2.compute.amazonaws.com:8000/auth_urls/login/
export const LOGIN_REQUEST_API = AMS_API + "/login/";

export const AIRLINE_LIST = AMS_API + "/airline-list/";

export const GATE_LIST = AMS_API + "/terminal-gate-list/";

export const PATCH_GATE_STATUS = AMS_API + "/terminal-gate-maintain/"

export const RUD_FLIGHT_SCHEDULE = AMS_API + "/flight-schedule-rud/"

export const PATCH_API = AMS_API + "/flight-schedule-rud/"

export const CREATE_FLIGHT = AMS_API + "/flight-schedule-create/";

export const MENU_ITEMS = {
    arrival : "ARRIVAL", 
    departure: "DEPARTURE", 
    dashboard: "DASHBOARD", 
    airlineManagement: "AIRLINE_MANAGEMENT",
    airportManagement: "AIRPORT_MANAGMENT",
    login: "LOGIN",
    logout: "LOGOUT",
    
}


