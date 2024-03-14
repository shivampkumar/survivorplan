import React from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, Typography, Card, CardContent } from '@mui/material';

const ReferencesDialog = ({ open, onClose, references }) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>References</DialogTitle>
      <DialogContent dividers>
        {references.map((ref, index) => (
          <Card key={index} variant="outlined" sx={{ mb: 2 }}>
            <CardContent>
              <Typography gutterBottom variant="h6" component="div">
                {ref.metadata.file_name} (Page {ref.metadata.page_label})
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {ref.text.split('. ').map((sentence, i) => (
                  <React.Fragment key={i}>
                    {sentence}.{i < ref.text.split('. ').length - 1 && <br />}
                  </React.Fragment>
                ))}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ReferencesDialog;
