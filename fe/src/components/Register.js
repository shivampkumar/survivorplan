import React, { useState } from 'react';
import { TextField, Button, Container, Typography, RadioGroup, FormControlLabel, Radio, Box } from '@mui/material';
import { AssignmentInd as AssignmentIndIcon } from '@mui/icons-material';

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
      <Box display="flex" flexDirection="column" alignItems="center" marginTop={8}>
        <AssignmentIndIcon color="primary" style={{ fontSize: 40, marginBottom: 20 }} />
        <Typography variant="h5" component="h1" gutterBottom>Register</Typography>
        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <TextField
            label="Email"
            type="email"
            variant="outlined"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Typography component="legend" style={{ marginTop: 20 }}>Role</Typography>
          <RadioGroup row value={role} onChange={(e) => setRole(e.target.value)} style={{ justifyContent: 'center' }}>
            <FormControlLabel value="patient" control={<Radio />} label="Patient" />
            <FormControlLabel value="doctor" control={<Radio />} label="Doctor" />
          </RadioGroup>
          <Button type="submit" fullWidth variant="contained" color="primary" style={{ marginTop: 20 }}>
            Register
          </Button>
        </form>
      </Box>
    </Container>
  );
}

export default Register;
