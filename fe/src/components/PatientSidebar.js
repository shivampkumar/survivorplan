import React from 'react';
import { Box, List, ListItem, Typography } from '@mui/material';

const PatientSidebar = ({ patients, onSelectPatient }) => {
  const getRandomColor = () => {
    const colors = ['#00C853', '#2196F3', '#F44336'];
    return colors[Math.floor(Math.random() * colors.length)];
  };

  return (
    <div style={{ width: '250px', borderRight: '1px solid #282828', backgroundColor: '#1E1E1E', color: '#FFFFFF' }}>
      <List>
        {patients.map((patient) => (
          <ListItem
            button
            key={patient.patientID}
            onClick={() => onSelectPatient(patient)}
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              '&:hover': {
                backgroundColor: '#282828',
              }
            }}
          >
            <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
              <Typography variant="body1" component="span" sx={{ mr: 1, color: '#FFFFFF' }}>
                {patient["Patient Name"]}
              </Typography>
              <Box
                component="span"
                sx={{
                  height: '10px',
                  width: '10px',
                  borderRadius: '50%',
                  display: 'inline-block',
                  bgcolor: getRandomColor(),
                }}
              />
            </Box>
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default PatientSidebar;
