import React from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, Typography, Card, CardContent } from '@mui/material';
import './ReferenceDialog.css';
import { Worker, Viewer, SpecialZoomLevel } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';

const ReferencesDialog = ({ open, onClose, references }) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle className="dialog-title">References</DialogTitle>
      <DialogContent dividers className="dialog-content">
        {references.map((reference, index) => (
          <Card key={index} className="reference-card">
            <CardContent>
              <Typography variant="h6" className="reference-title">File: {reference.metadata.file_name}</Typography>
              <Typography variant="body1" className="reference-page">Page: {reference.metadata.page_label}</Typography>
              <Typography variant="body2" className="reference-text" style={{ marginTop: '10px' }}>
                {reference.text}
              </Typography>
              {/* Uncomment to render PDFs */}
              {/* {renderPDF(`/resources/${reference.metadata.file_name}`)} */}
            </CardContent>
          </Card>
        ))}
      </DialogContent>
      <DialogActions className="dialog-actions">
        <Button onClick={onClose} className="close-button">Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ReferencesDialog;
