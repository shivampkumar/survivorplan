import React, { useState, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, Typography, Card, CardContent } from '@mui/material';
import { Document } from 'react-pdf'; 

const ReferencesDialog = ({ open, onClose, references }) => {
  const [pdfUrls, setPdfUrls] = useState([]); // Store URLs of referenced PDFs
  const [highlightedTexts, setHighlightedTexts] = useState([]); // Store highlighted text for each PDF

  useEffect(() => {
    // Create PDF URLs from file names in references
    const pdfUrls = references.map((ref) => `/resources/${ref.metadata.file_name}`);
    setPdfUrls(pdfUrls);

    // Initialize empty highlighted texts array
    const initialHighlightedTexts = references.map(() => []);
    setHighlightedTexts(initialHighlightedTexts);
  }, [references]);

  const handleHighlight = (pageIndex, text, pdfIndex) => {
    const updatedHighlights = [...highlightedTexts];
    updatedHighlights[pdfIndex] = [...updatedHighlights[pdfIndex], { text, pageIndex }];
    setHighlightedTexts(updatedHighlights);
  };
  console.log("ReferencesDialog.js: references", references)

  const renderPDF = (pdfUrl, pdfIndex) => {
    return (
      <div key={pdfUrl}>
        <Typography variant="h6">{references[pdfIndex].metadata.file_name}</Typography>
        <Document
          file={pdfUrl}
          onLoadSuccess={(pdf) => {
            const searchText = references[pdfIndex].text;
            pdf.find(searchText, { pageNumber: references[pdfIndex].metadata.page_label }); // Search on specific page
          }}
        />
      </div>
    );
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>References</DialogTitle>
      <DialogContent dividers>
        {pdfUrls.map((pdfUrl, pdfIndex) => renderPDF(pdfUrl, pdfIndex))}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ReferencesDialog2;
