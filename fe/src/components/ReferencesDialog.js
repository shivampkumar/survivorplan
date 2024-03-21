import React, { useState, useEffect } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button } from '@mui/material';
import { PdfHighlighter, Tip, Highlight, Popup, PdfLoader } from 'react-pdf-highlighter';

// Adjust this base URL according to where your component is located relative to the resources folder
const baseURL = '/resources/';

const ReferencesDialog = ({ open, onClose, references }) => {
  const [currentPdf, setCurrentPdf] = useState(null);

  useEffect(() => {
    // Assuming the first reference is selected by default
    if (references.length > 0) {
      const firstRef = references[0];
      const pdfUrl = `${baseURL}${firstRef.metadata.file_name}`;
      setCurrentPdf({
        url: pdfUrl,
        highlights: [] // You would populate this with actual highlight data if available
      });
    }
  }, [references]);

  const addHighlight = (highlight) => {
    // Logic to add a new highlight
    console.log("Adding highlight:", highlight);
  };

  const renderPdfHighlighter = (pdfData) => {
    if (!pdfData) return <div>Loading...</div>;

    return (
      <PdfLoader url={pdfData.url} beforeLoad={<div>Loading...</div>}>
        {(pdfDocument) => (
          <PdfHighlighter
            pdfDocument={pdfDocument}
            enableAreaSelection={(event) => event.altKey}
            onSelectionFinished={(position, content, hideTipAndSelection, transformSelection) => (
              <Tip
                onOpen={transformSelection}
                onConfirm={(comment) => {
                  addHighlight({ content, position, comment });
                  hideTipAndSelection();
                }}
              />
            )}
            highlightTransform={(highlight, index, setTip, hideTip, viewportToScaled, screenshot, isScrolledTo) => {
              return (
                <Popup
                  popupContent={<div>Highlight Popup</div>}
                  onMouseOver={(popupContent) => setTip(highlight, () => popupContent)}
                  onMouseOut={hideTip}
                  key={index}
                  children={<Highlight isScrolledTo={isScrolledTo} position={highlight.position} />}
                />
              );
            }}
            highlights={pdfData.highlights}
          />
        )}
      </PdfLoader>
    );
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>References</DialogTitle>
      <DialogContent dividers style={{ height: "80vh" }}>
        <div style={{ height: "100%" }}>
          {currentPdf && renderPdfHighlighter(currentPdf)}
        </div>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ReferencesDialog;
