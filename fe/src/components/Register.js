import React, { useState } from 'react';
import { TextField, Button, Container, Typography, RadioGroup, FormControlLabel, Radio } from '@mui/material';

function Register({ onRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('patient');

  const handleSubmit = async (event) => {
    event.preventDefault();
    onRegister(email, password, role);
  };

  return (
    <Container maxWidth="xs">
      <form onSubmit={handleSubmit}>
        <Typography variant="h4">Register</Typography>
        <TextField
          label="Email"
          type="email"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Typography component="legend">Role</Typography>
        <RadioGroup row value={role} onChange={(e) => setRole(e.target.value)}>
          <FormControlLabel value="patient" control={<Radio />} label="Patient" />
          <FormControlLabel value="doctor" control={<Radio />} label="Doctor" />
        </RadioGroup>
        <Button type="submit" fullWidth variant="contained" color="primary">
          Register
        </Button>
      </form>
    </Container>
  );
}

export default Register;
