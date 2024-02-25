import React, { useState } from 'react';
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

  const handleLogin = async (email, password) => {
    try {
      const response = await axios.post('http://20.168.8.23:8080/api/login', { email, password });
      console.log(response.data);
      alert('Login successful');
      setUserRole(response.data.role); // Assuming the role is returned in the login response
      setIsLoggedIn(true);
    } catch (error) {
      console.error(error);
      alert('Login failed');
    }
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
          return <DoctorView />;
        case 'patient':
          return <PatientView />;
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
