import React from 'react';
import { List, ListItem, ListItemText } from '@mui/material';

const PatientSidebar = ({ patients, onSelectPatient }) => {
  console.log(patients);
  return (
    <div style={{ width: '250px', borderRight: '1px solid #ccc' }}>
      <List>
        {patients.map((patient) => (
          <ListItem button key={patient.patientID} onClick={() => onSelectPatient(patient)}>
            <ListItemText primary={patient["General Information"]["Patient Name"]} />
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default PatientSidebar;
