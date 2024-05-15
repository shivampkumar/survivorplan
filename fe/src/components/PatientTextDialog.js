import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

const PatientTextDialog = ({ open, onClose, patientText }) => {
  console.log("Patient Text", patientText);
  // Patient text is a json with values separated by '||'. Convert it to a list of paragraphs and then use
  // it in the dialog
  //convert json to string first and then split it by '||'
  patientText = JSON.stringify(patientText);
  const formatPatientText = (patientText) => {
    if (patientText) {
      const paragraphs = patientText.split('||');
      return paragraphs.map((paragraph, index) => (
        <Typography key={index} variant="body1" paragraph>{paragraph}</Typography>
      ));
    }
  };
  return (
    <Dialog open={open} onClose={onClose} fullWidth>
      <DialogTitle>
        <Typography variant="h5">Patient Information</Typography>
      </DialogTitle>
      <DialogContent>
        {formatPatientText(patientText)}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">Close</Button>
      </DialogActions>
    </Dialog>
  );
};


  

export default PatientTextDialog;
