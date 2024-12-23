import React, { useState } from 'react';
import { Card, CardContent, Typography, Grid, Box, TextField, Button } from '@mui/material';
import PhoneIcon from '@mui/icons-material/Phone';
import EmailIcon from '@mui/icons-material/Email';
import CakeIcon from '@mui/icons-material/Cake';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import PersonIcon from '@mui/icons-material/Person';

const PatientInfo = ({ patientDetails }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [details, setDetails] = useState({
    "Patient Name": patientDetails["Patient Name"] || "",
    "Date of Birth": patientDetails["Date of Birth"] || "",
    "Contact Number": patientDetails["Contact Number"] || "",
    "Email": patientDetails["Email"] || "",
    "Cancer Type": patientDetails["Cancer Type"] || "",
    "Stage": patientDetails["Stage"] || "",
    "Diagnosis Date": patientDetails["Diagnosis Date"] || "",
  });

  const infoFields = [
    { key: "Patient Name", icon: <PersonIcon /> },
    { key: "Date of Birth", icon: <CakeIcon /> },
    { key: "Contact Number", icon: <PhoneIcon /> },
    { key: "Email", icon: <EmailIcon /> },
    { key: "Cancer Type", icon: <LocalHospitalIcon /> },
    { key: "Stage", icon: <LocalHospitalIcon /> },
    { key: "Diagnosis Date", icon: <LocalHospitalIcon /> }
  ];

  const handleEditClick = () => {
    setIsEditing(!isEditing);
    if (isEditing) {
      console.log("Changes saved", details);
    }
  };

  const handleChange = (key, value) => {
    setDetails(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <Card variant="outlined" sx={{ marginBottom: '20px', backgroundColor: '#282828', color: '#FFFFFF', width: '100%' }}>
      <CardContent>
        <Typography variant="h5" gutterBottom align="center" sx={{ color: '#FFC107' }}>
          <strong>General Information</strong>
        </Typography>
        
        <Box sx={{ marginBottom: '16px' }}>
          {infoFields.map(({ key, icon }) => (
            <Grid container alignItems="center" key={key} sx={{ marginBottom: '8px' }}>
              <Grid item sx={{ marginRight: '8px' }}>{icon}</Grid>
              <Grid item sx={{ flexGrow: 1 }}>
                {isEditing ? (
                  <TextField
                    value={details[key] || ''}
                    onChange={(e) => handleChange(key, e.target.value)}
                    label={key}
                    variant="outlined"
                    size="small"
                    fullWidth
                    sx={{ 
                      input: { color: '#FFFFFF' },
                      '& .MuiOutlinedInput-root': {
                        '& fieldset': {
                          borderColor: '#FFFFFF3B',
                        },
                        '&:hover fieldset': {
                          borderColor: '#FFFFFF7F',
                        },
                      },
                      '& .MuiInputLabel-root': {
                        color: '#FFFFFFB3',
                      }
                    }}
                  />
                ) : (
                  <Typography variant="body1">
                    <strong>{key}:</strong> {details[key] || 'N/A'}
                  </Typography>
                )}
              </Grid>
            </Grid>
          ))}
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <Button 
            variant="contained" 
            sx={{ 
              backgroundColor: '#007BFF', 
              color: '#FFFFFF',
              '&:hover': {
                backgroundColor: '#0056b3',
              }
            }} 
            onClick={handleEditClick}
          >
            {isEditing ? 'Save' : 'Edit'}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default PatientInfo;
