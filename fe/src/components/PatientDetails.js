import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

// Example data, replace with dynamic data fetched based on selected patient
const patientInfo = {
  "General Information": { /* ... */ },
  "Treatment Summary": { /* ... */ }
};

const PatientDetails = ({ patient }) => {
  return (
    <div style={{ flex: 1, overflow: 'auto', padding: '20px' }}>
      <Typography variant="h4" gutterBottom>{patient.name}'s Details</Typography>
      
      {/* General Information */}
      <Card variant="outlined" style={{ marginBottom: '20px' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>General Information</Typography>
          {Object.entries(patientInfo["General Information"]).map(([key, value]) => (
            <Typography key={key}>{`${key}: ${value}`}</Typography>
          ))}
        </CardContent>
      </Card>
      
      {/* Treatment Summary */}
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h5" gutterBottom>Treatment Summary</Typography>
          {/* Nested mapping for each section */}
        </CardContent>
      </Card>
    </div>
  );
};

export default PatientDetails;
