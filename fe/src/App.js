import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import DoctorView from './components/DoctorView';
import PatientView from './components/PatientView';
import axios from 'axios';
import Header from './components/Header';
import { Button } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import { createTheme } from '@mui/material/styles';
import { Tabs, Tab, Box, Typography } from '@mui/material';

const theme = createTheme({
  palette: {
    navyBlue: {
      main: '#003366', // A common shade for navy blue
      light: '#3E4E88', // Lighter shade of navy blue
      dark: '#001D4A', // Darker shade of navy blue
      contrastText: '#FFFFFF', // White color for contrasting text
    },
  },
});


function App() {
  const [isLoginView, setIsLoginView] = useState(true);
  const [userRole, setUserRole] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [patientDetails, setPatientDetails] = useState(null); // New state for patient details
  const [patients, setPatients] = useState([]); // State to store patient list
  const [loggedInPatient, setLoggedInPatient] = useState(null); // State to store logged-in patient details

  const API_BASE_URL = 'http://20.168.8.23:8080/api';

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  // Fetch patient details for the logged-in patient and set patient details state

  useEffect(() => {
    if (isLoggedIn && userRole === 'doctor') {
      axios.get(`${API_BASE_URL}/patientsFH`)
        .then(response => {
          setPatients(response.data); // Assuming API returns an array of patients
        })
        .catch(error => console.error("Failed to fetch patients", error));
    }
  }, [isLoggedIn, userRole]);

  const handleLogin = async (email, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, { email, password });
      console.log(response.data);
      setUserRole(response.data.role); // Set user role from response

      // If the role is 'patient', fetch and set patient details
      if (response.data.role === 'patient') {
        // Assuming the response includes patientID for patients
        const patientID = response.data.patientID;
        fetchAndSetPatientDetails(patientID);
      }

      setIsLoggedIn(true);
    } catch (error) {
      console.error(error);
      alert('Login failed');
    }
  };

  // Function to fetch and set patient details
  const fetchAndSetPatientDetails = (patientID) => {
    console.log("Fetching patient details for patient ID:", patientID)
    axios.get(`${API_BASE_URL}/patients/${patientID}`)
      .then((response) => {
        setPatientDetails(response.data);
        console.log("Fetched patient details:", response.data);
        setLoggedInPatient(response.data); // Store the logged-in patient's details
      })
      .catch((error) => {
        console.error("Failed to fetch patient details", error);
      });
  };

  const handleRegister = async (email, password, role) => {
    try {
      const response = await axios.post('http://20.168.8.23:8080/api/register', {
        email,
        password,
        role,
      });
      console.log(response.data);
      // Handle registration success
    } catch (error) {
      console.error(error);
      // Handle registration failure
    }
  };

  const renderUserView = () => {
    if (!isLoggedIn) {
      return (
        <Box display="flex" flexDirection="column" alignItems="center" marginTop={8}>
          <Tabs value={tabValue} onChange={handleTabChange} centered>
            <Tab label="Login" />
            <Tab label="Register" />
          </Tabs>
          {tabValue === 0 && <Login onLogin={handleLogin} />}
          {tabValue === 1 && <Register onRegister={handleRegister} />}
          {/* Add a Link to navigate to the doctor's site */}
        </Box>
      );
    } else {
      switch (userRole) {
        case 'doctor':
          return <DoctorView patients={patients} />;
        case 'patient':
          // Assuming you fetch and set individual patient details in a similar useEffect hook based on the logged-in patient ID
          return <PatientView patientDetails={patientDetails} />;
        default:
          return <div>Role not recognized</div>;
      }
    }
  };

  return (
    <div>
      <Header />
      {renderUserView()}
    </div>
  );
}

export default App;
