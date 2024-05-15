import React, { useState } from 'react';
import { Card, CardContent, Typography, Grid, Box, TextField, Button } from '@mui/material';
import PhoneIcon from '@mui/icons-material/Phone';
import EmailIcon from '@mui/icons-material/Email';
import CakeIcon from '@mui/icons-material/Cake';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import PersonIcon from '@mui/icons-material/Person';

const PatientInfo = ({ patientDetails }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [details, setDetails] = useState(patientDetails);

  // Define the keys and their display order
  const personalInfoKeys = ['Patient Name', 'Patient DOB', 'Patient Email', 'Patient Phone Number'];
  const providerKeys = ['Primary Care Provider', 'Surgeon', 'Radiation Oncologist', 'Medical Oncologist', 'Other Providers'];

  // Function to return the appropriate icon for each key
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

  const handleEditClick = () => {
    setIsEditing(!isEditing);
    if (isEditing) {
      // TODO: Save changes via API
      console.log("Changes saved", details);
    }
  };

  const handleChange = (key, value) => {
    setDetails((prevDetails) => ({
      ...prevDetails,
      [key]: value,
    }));
  };

  return (
    <Card variant="outlined" sx={{ marginBottom: '20px' }}>
      <CardContent>
      <Typography variant="h5" gutterBottom align="center"><strong>General Information</strong></Typography>
        <Box sx={{ marginBottom: '16px' }}>
          <Typography variant="h6" gutterBottom>Personal Information</Typography>
          {personalInfoKeys.map((key) => (
            <Grid container alignItems="center" key={key} sx={{ marginBottom: '8px' }}>
              <Grid item sx={{ marginRight: '8px' }}>{IconByKey(key)}</Grid>
              <Grid item>
                {isEditing ? (
                  <TextField
                    value={details[key]}
                    onChange={(e) => handleChange(key, e.target.value)}
                    label={key.replace('Patient ', '')}
                    variant="outlined"
                    size="small"
                  />
                ) : (
                  <Typography variant="body1"><strong>{key.replace('Patient ', '')}:</strong> {details[key]}</Typography>
                )}
              </Grid>
            </Grid>
          ))}
        </Box>
        <Box>
          <Typography variant="h6" gutterBottom>Health Care Providers</Typography>
          {providerKeys.map((key) => (
            <Grid container alignItems="center" key={key} sx={{ marginBottom: '8px' }}>
              <Grid item sx={{ marginRight: '8px' }}><LocalHospitalIcon /></Grid>
              <Grid item>
                {isEditing ? (
                  <TextField
                    value={details[key]}
                    onChange={(e) => handleChange(key, e.target.value)}
                    label={key}
                    variant="outlined"
                    size="small"
                  />
                ) : (
                  <Typography variant="body1"><strong>{key}:</strong> {details[key]}</Typography>
                )}
              </Grid>
            </Grid>
          ))}
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <Button variant="contained" color="primary" onClick={handleEditClick}>
            {isEditing ? 'Save' : 'Edit'}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default PatientInfo;
