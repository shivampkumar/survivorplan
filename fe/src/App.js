import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import DoctorView from './components/DoctorView';
import PatientView from './components/PatientView';
import axios from 'axios';
import Header from './components/Header';
import { Button } from '@mui/material';

function App() {
  const [isLoginView, setIsLoginView] = useState(true);
  const [userRole, setUserRole] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [patientDetails, setPatientDetails] = useState(null); // New state for patient details
  const [patients, setPatients] = useState([]); // State to store patient list
  const [loggedInPatient, setLoggedInPatient] = useState(null); // State to store logged-in patient details

  const API_BASE_URL = 'http://20.168.8.23:8080/api';

  // Fetch patient details for the logged-in patient and set patient details state

  useEffect(() => {
    if (isLoggedIn && userRole === 'doctor') {
      axios.get(`${API_BASE_URL}/patients`)
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
      alert('Login successful');
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
    axios.get(`${API_BASE_URL}/patients/${patientID}`)
      .then((response) => {
        setPatientDetails(response.data);
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
        <>
          {isLoginView ? (
            <>
              <Login onLogin={handleLogin} />
              <Button onClick={() => setIsLoginView(false)}>Go to Register</Button>
            </>
          ) : (
            <>
              <Register onRegister={handleRegister} />
              <Button onClick={() => setIsLoginView(true)}>Go to Login</Button>
            </>
          )}
        </>
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
