// PatientTextDialog.js

import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button } from '@mui/material';

const PatientTextDialog = ({ open, handleClose, patientText }) => {
  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>Relevant Patient Text</DialogTitle>
      <DialogContent>
        <DialogContentText>
          {patientText}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default PatientTextDialog;
