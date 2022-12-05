import * as React from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MainListItems from './listItems';
import AirlineEmployeeListItems from './AirlineEmployeeMenuList';
import AirportEmployeeListItems from './AirPortEmployeeMenuList';
import MainView from '../FrontPage/MainView';
import Arrival from '../FlightSchedule/Arrival';
import Departure from '../FlightSchedule/Departure';
import Login from '../Login/Login';
import GateManagement from '../GateSelector';
import AirlineManagementPage from '../AirlineManagement/AirlineManagementPage';

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

const mdTheme = createTheme();

function DashboardContent() {
  const [open, setOpen] = React.useState(false);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  const [selectedMenuItem, setSelectedMenuItem] = React.useState("dashboard")

  let content;
  if (selectedMenuItem == "dashboard") {
    content = <MainView selected={selectedMenuItem} setSelected={setSelectedMenuItem}/>
  } else if (selectedMenuItem === "arrivals") {
    content = <Arrival screen="arrival"/>
  } else if (selectedMenuItem === "departures") {
    content = <Departure screen="departures"/>
  } else if (selectedMenuItem === "login") {
    content = <Login />
  } else if (selectedMenuItem === "aboutus") {
    content = <>ABOUT US</>
  }  else if (selectedMenuItem === "airlineManagement") {
    content = <AirlineManagementPage />
  }  else if (selectedMenuItem === "gateManagement") {
    content = <GateManagement />
  } else if (selectedMenuItem === "logout"){
    window.sessionStorage.clear();
    window.location.reload();
  }

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar position="absolute" open={open}>
          <Toolbar
            sx={{
              pr: '24px', // keep right padding when drawer closed
            }}
          >
            <IconButton
              edge="start"
              color="inherit"
              aria-label="open drawer"
              onClick={toggleDrawer}
              sx={{
                marginRight: '36px',
                ...(open && { display: 'none' }),
              }}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Dashboard
            </Typography>
            <IconButton color="inherit">
              <Badge badgeContent={4} color="secondary">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Toolbar>
        </AppBar>
        <Drawer variant="permanent" open={open}>
          <Toolbar
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              px: [1],
            }}
          >
            <IconButton onClick={toggleDrawer}>
              <ChevronLeftIcon />
            </IconButton>
          </Toolbar>
          <Divider />
          <List component="nav">
            {setMenuForUser(selectedMenuItem, setSelectedMenuItem)}
            <Divider sx={{ my: 1 }} />
          </List>
        </Drawer>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          {/* <>Content goes here</> */}
          {content}
        </Box>
      </Box>
    </ThemeProvider>
  );
}

const setMenuForUser = (selectedMenuItem, setSelectedMenuItem) => {
  let user_role = window.sessionStorage.getItem("user_role");
  if (user_role === "airline_employee") {
    return (
      <AirlineEmployeeListItems selected={selectedMenuItem} setSelected={setSelectedMenuItem} />
    )
  } else if (user_role === "airport_employee") {
    return (
      <AirportEmployeeListItems selected={selectedMenuItem} setSelected={setSelectedMenuItem} />
    )
  } else {
    return (
      <MainListItems selected={selectedMenuItem} setSelected={setSelectedMenuItem} />
    )
  }
}

export default function Dashboard() {
  return <DashboardContent />;
}