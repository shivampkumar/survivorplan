import React from 'react';
import { Box, List, ListItem } from '@mui/material';

const PatientSidebar = ({ patients, onSelectPatient }) => {
  // Function to get a random color
  const getRandomColor = () => {
    const colors = ['#00C853', '#2196F3', '#F44336']; // Green, Blue, Red
    return colors[Math.floor(Math.random() * colors.length)];
  };

  return (
    <div style={{ width: '250px', borderRight: '1px solid #ccc' }}>
      <List>
        {patients.map((patient) => (
          <ListItem 
            button 
            key={patient.patientID} 
            onClick={() => onSelectPatient(patient)} 
            sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
          >
            <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
              {/* Patient name */}
              <Box component="span" sx={{ mr: 1 }}>
                {patient["General Information"]["Patient Name"]}
              </Box>
              
              {/* Dot */}
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
