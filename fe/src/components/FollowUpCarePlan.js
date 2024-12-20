import React, { useState } from 'react';
import { Button, Card, CardContent, Grid, Table, TableBody, IconButton, TableCell, TableHead, TableRow, Typography, TextField, Tooltip, Checkbox } from '@mui/material';
import ReferencesDialog from './ReferencesDialog';
import InfoIcon from '@mui/icons-material/Info';
import './FollowUpCarePlan.css';

const FollowUpCarePlan = ({ data }) => {
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReferences, setCurrentReferences] = useState([]);
  const [verifiedRows, setVerifiedRows] = useState({});

  if (!data) return <div>Loading...</div>;

  const handleOpenDialog = (contextId) => {
    // Get context from retrieved_context using contextId
    const references = data.retrieved_context ? [data.retrieved_context[contextId]] : [];
    setCurrentReferences(references);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleVerificationChange = (path) => {
    setVerifiedRows((prevVerifiedRows) => ({
      ...prevVerifiedRows,
      [path]: !prevVerifiedRows[path],
    }));
  };

  const renderSectionRows = (items, sectionKey) => {
    if (!items || !Array.isArray(items)) return null;

    const getTableCells = (item) => {
      switch (sectionKey) {
        case "Cancer surveillance and other recommended tests":
          return (
            <>
              <TableCell>{item["Test type"]}</TableCell>
              <TableCell>{item["When / how often"]}</TableCell>
              <TableCell>{item["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(item["Retrieved context id"])}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`${sectionKey}.${item["Test type"]}`] || false}
                  onChange={() => handleVerificationChange(`${sectionKey}.${item["Test type"]}`)}
                />
              </TableCell>
            </>
          );

        case "Lifestyle and behavior recommendations":
          return (
            <>
              <TableCell>{item["Lifestyle"]}</TableCell>
              <TableCell>{item["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(item["Retrieved context id"])}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`${sectionKey}.${item["Lifestyle"]}`] || false}
                  onChange={() => handleVerificationChange(`${sectionKey}.${item["Lifestyle"]}`)}
                />
              </TableCell>
            </>
          );

        case "Possible late and long-term effects":
          return (
            <>
              <TableCell>{item["Treatment effect"]}</TableCell>
              <TableCell>{item["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(item["Retrieved context id"])}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`${sectionKey}.${item["Treatment effect"]}`] || false}
                  onChange={() => handleVerificationChange(`${sectionKey}.${item["Treatment effect"]}`)}
                />
              </TableCell>
            </>
          );

        case "References to helpful resources":
          return (
            <>
              <TableCell>{item["Resource"]}</TableCell>
              <TableCell>{item["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(item["Retrieved context id"])}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`${sectionKey}.${item["Resource"]}`] || false}
                  onChange={() => handleVerificationChange(`${sectionKey}.${item["Resource"]}`)}
                />
              </TableCell>
            </>
          );

        default:
          return (
            <>
              <TableCell>{item["Issue"] || item["Symptom"]}</TableCell>
              <TableCell>{item["Explanation"]}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleOpenDialog(item["Retrieved context id"])}>
                  <InfoIcon />
                </IconButton>
              </TableCell>
              <TableCell>
                <Checkbox
                  checked={verifiedRows[`${sectionKey}.${item["Issue"] || item["Symptom"]}`] || false}
                  onChange={() => handleVerificationChange(`${sectionKey}.${item["Issue"] || item["Symptom"]}`)}
                />
              </TableCell>
            </>
          );
      }
    };

    return items.map((item, index) => (
      <TableRow key={index}>
        {getTableCells(item)}
      </TableRow>
    ));
  };

  const getTableHeaders = (sectionKey) => {
    switch (sectionKey) {
      case "Cancer surveillance and other recommended tests":
        return (
          <TableRow>
            <TableCell>Test Type</TableCell>
            <TableCell>When/How Often</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Validate</TableCell>
          </TableRow>
        );
      default:
        return (
          <TableRow>
            <TableCell>Description</TableCell>
            <TableCell>Explanation</TableCell>
            <TableCell>References</TableCell>
            <TableCell>Validate</TableCell>
          </TableRow>
        );
    }
  };

  return (
    <div className="follow-up-care-plan-container">
      <Typography variant="h4" className="follow-up-care-plan-title">
        Follow-up Care Plan
      </Typography>

      <Grid container spacing={2}>
        {Object.entries(data).map(([sectionKey, sectionData]) => {
          // Skip the retrieved_context section as it's used for references
          if (sectionKey === 'retrieved_context') return null;

          return (
            <Grid item xs={12} key={sectionKey}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{sectionKey}</Typography>
                  <Table>
                    <TableHead>
                      {getTableHeaders(sectionKey)}
                    </TableHead>
                    <TableBody>
                      {renderSectionRows(sectionData, sectionKey)}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <ReferencesDialog
        open={openDialog}
        onClose={handleCloseDialog}
        references={currentReferences}
      />
    </div>
  );
};

export default FollowUpCarePlan;
