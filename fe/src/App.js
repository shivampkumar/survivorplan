import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import axios from 'axios';
import { Button } from '@mui/material';

function App() {
  const [isLoginView, setIsLoginView] = useState(true);

  const handleLogin = async (email, password) => {
    try {
      const response = await axios.post('http://localhost:8080/api/login', { 
        email, 
        password 
      });
      console.log(response.data);
      alert('Login successful');
      // Further actions on successful login (e.g., redirect, save token)
    } catch (error) {
      console.error(error.response ? error.response.data : error);
      alert('Login failed');
    }
  };

  const handleRegister = async (email, password, role) => {
    try {
      const response = await axios.post('http://localhost:8080/api/register', {
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

  return (
    <div>
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
    </div>
  );
}

export default App;
