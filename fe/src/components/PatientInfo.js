import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const PatientInfo = ({ patientDetails }) => {
  return (
    <Card variant="outlined" style={{ marginBottom: '20px' }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>General Information</Typography>
        {Object.entries(patientDetails).map(([key, value]) => (
          <Typography key={key}>{`${key}: ${value}`}</Typography>
        ))}
      </CardContent>
    </Card>
  );
};

export default PatientInfo;
