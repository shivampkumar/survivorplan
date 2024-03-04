import React from 'react';
import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
import PhoneIcon from '@mui/icons-material/Phone';
import EmailIcon from '@mui/icons-material/Email';
import CakeIcon from '@mui/icons-material/Cake';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import PersonIcon from '@mui/icons-material/Person';

const PatientInfo = ({ patientDetails }) => {
  const personalInfoKeys = ['Patient Name', 'Patient DOB', 'Patient Phone Number', 'Patient Email'];
  const providerKeys = ['Primary Care Provider', 'Surgeon', 'Radiation Oncologist', 'Medical Oncologist', 'Other Providers'];

  const IconByKey = (key) => {
    switch (key) {
      case 'Patient Phone Number':
        return <PhoneIcon />;
      case 'Patient Email':
        return <EmailIcon />;
      case 'Patient DOB':
        return <CakeIcon />;
      default:
        return <PersonIcon />;
    }
  };

  return (
    <Card variant="outlined" sx={{ marginBottom: '20px' }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>General Information</Typography>
        <Box sx={{ marginBottom: '16px' }}>
          <Typography variant="h6" gutterBottom>Personal Information</Typography>
          {Object.entries(patientDetails)
            .filter(([key]) => personalInfoKeys.includes(key))
            .map(([key, value]) => (
              <Grid container alignItems="center" key={key}>
                <Grid item sx={{ marginRight: '8px' }}>{IconByKey(key)}</Grid>
                <Grid item>
                  <Typography variant="body1"><strong>{key}:</strong> {value}</Typography>
                </Grid>
              </Grid>
            ))}
        </Box>
        <Box>
          <Typography variant="h6" gutterBottom>Medical Team</Typography>
          {Object.entries(patientDetails)
            .filter(([key]) => providerKeys.includes(key))
            .map(([key, value]) => (
              <Grid container alignItems="center" key={key}>
                <Grid item sx={{ marginRight: '8px' }}><LocalHospitalIcon /></Grid>
                <Grid item>
                  <Typography variant="body1"><strong>{key}:</strong> {value}</Typography>
                </Grid>
              </Grid>
            ))}
        </Box>
      </CardContent>
    </Card>
  );
};

export default PatientInfo;
