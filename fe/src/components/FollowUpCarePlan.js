// FollowUpCarePlan.js

import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, Grid, Table, TableBody, Checkbox, TableCell, TableHead, TableRow, Typography, TextField, Tooltip, IconButton } from '@mui/material';
import ReferencesDialog from './ReferencesDialog';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';
import './FollowUpCarePlan.css';

const API_BASE_URL = 'http://20.168.8.23:8080/api';

// Generate consistent row IDs based on content
const generateRowID = (sectionKey, item) => {
  const content = JSON.stringify(item);
  let hash = 0;
  if (content.length === 0) return hash.toString();
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return `${sectionKey}-${hash.toString()}`;
};

const FollowUpCarePlan = ({ followUpCarePlan, validations, patientID }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedPlan, setEditedPlan] = useState({});
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReferences, setCurrentReferences] = useState([]);
  const [verifiedRows, setVerifiedRows] = useState({});
  const [dateValues, setDateValues] = useState({});
  const [validationData, setValidationData] = useState({});

  useEffect(() => {
    setEditedPlan(followUpCarePlan);
    if (validations) {
      setValidationData(validations);
      const initialVerifiedRows = {};
      for (const rowID in validations) {
        initialVerifiedRows[rowID] = validations[rowID].verified;
      }
      setVerifiedRows(initialVerifiedRows);
    }
  }, [followUpCarePlan, validations]);

  const handleOpenDialog = (fileNames, pageLabels, sectionKey) => {
    const sectionContext = editedPlan[sectionKey]?.context || [];
    const references = sectionContext.filter(contextItem =>
      fileNames.includes(contextItem.metadata.file_name) &&
      pageLabels.map(String).includes(contextItem.metadata.page_label.toString())
    );
    setCurrentReferences(references);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
  };

  const handleVerificationChange = (rowID) => {
    setVerifiedRows((prevVerifiedRows) => ({
      ...prevVerifiedRows,
      [rowID]: !prevVerifiedRows[rowID],
    }));
  };

  const handleEditClick = () => {
    if (isEditing) {
      // Save validations before switching to non-edit mode
      handleSaveValidations();
    }
    setIsEditing(!isEditing);
  };

  const handleScoreChange = (rowID, value) => {
    setValidationData((prevData) => ({
      ...prevData,
      [rowID]: {
        ...prevData[rowID],
        score: value,
      },
    }));
  };

  const handleCommentChange = (rowID, value) => {
    setValidationData((prevData) => ({
      ...prevData,
      [rowID]: {
        ...prevData[rowID],
        comment: value,
      },
    }));
  };

  const handleChange = (path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const lastObj = keys.reduce((obj, key) => obj[key], editedPlan);
    lastObj[lastKey] = value;
    setEditedPlan({ ...editedPlan });
  };

  const handleDateChange = (path, newValue) => {
    setDateValues((prev) => ({
      ...prev,
      [path]: newValue,
    }));
  };

  const handleSaveValidations = () => {
    const validationList = [];
    for (const rowID in validationData) {
      const data = validationData[rowID];
      validationList.push({
        row_id: rowID,
        score: data.score,
        comment: data.comment,
        verified: verifiedRows[rowID] || false,
      });
    }
    if (validationList.length > 0) {
      axios.post(`${API_BASE_URL}/patients/${patientID}/validate`, { validations: validationList })
        .then(response => {
          console.log('Validation data saved', response.data);
        })
        .catch(error => {
          console.error('Failed to save validation data', error);
        });
    }
  };

  const renderEditableField = (path, value) => (
    isEditing ? (
      <TextField
        value={value}
        onChange={(e) => handleChange(path, e.target.value)}
        fullWidth
        variant="outlined"
        size="small"
      />
    ) : (
      <Typography variant="body2">{value}</Typography>
    )
  );

  const renderVerificationCheckbox = (rowID) => (
    <Checkbox
      checked={!!verifiedRows[rowID]}
      onChange={() => handleVerificationChange(rowID)}
      disabled={!isEditing}
    />
  );

  const renderInfoButton = (item, sectionKey) => (
    <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"], sectionKey)}>i</Button>
  );

  // Date functions
  const getRandomDate = (start, end) => {
    const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    return date;
  };

  const getRandomLastVisitDate = () => {
    const startDate = new Date('2023-01-01');
    const endDate = new Date('2024-07-31');
    return getRandomDate(startDate, endDate);
  };

  const getRandomNextVisitDate = () => {
    const startDate = new Date('2024-08-31');
    const endDate = new Date('2025-12-31');
    return getRandomDate(startDate, endDate);
  };

  const renderSectionRows = (section, sectionKey) => (
    section.map((item, index) => {
      const rowID = generateRowID(sectionKey, item);
      const validation = validationData[rowID] || {};
      const rowClass = verifiedRows[rowID] ? 'table-row verified' : 'table-row';
      const nextVisitDatePath = `visit.${index}.nextVisitDate`;

      return (
        <TableRow key={rowID} className={rowClass}>
          <TableCell>{renderEditableField(`${sectionKey}.recommendation.${sectionKey}.${index}.Visit type`, item["Visit type"] || item["Test type"] || item["Treatment effect"] || item["Issue"] || item["Lifestyle"] || item["Resource"])}</TableCell>
          {sectionKey === "Cancer Surveillance or Other Recommended Tests" && (
            <TableCell>{renderEditableField(`${sectionKey}.recommendation.${sectionKey}.${index}.Coordinating provider`, item["Coordinating provider"])}</TableCell>
          )}
          {"When / how often" in item && (
            <TableCell>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', width: '100%' }}>
                <div style={{ marginBottom: '8px' }}>
                  <Typography variant="body2" style={{ color: 'white' }}>
                    Last Visit Date: {new Date(getRandomLastVisitDate()).toLocaleDateString()}
                  </Typography>
                </div>
                <Typography variant="body2" style={{ color: 'white' }}>
                  Suggested Next Visit Date:
                </Typography>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <DatePicker
                    value={dateValues[nextVisitDatePath] || new Date(getRandomNextVisitDate())}
                    onChange={(newValue) => handleDateChange(nextVisitDatePath, newValue)}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        size="small"
                        fullWidth
                        style={{
                          minWidth: '200px',
                          backgroundColor: '#333', // Dark background for input field
                          color: 'white' // White text for input field
                        }}
                        InputLabelProps={{ style: { color: 'white' } }} // White label text
                        InputProps={{
                          style: {
                            color: 'white' // White input text
                          },
                          endAdornment: (
                            <IconButton>
                              {params.InputProps.endAdornment}
                            </IconButton>
                          ),
                        }}
                      />
                    )}
                  />
                </LocalizationProvider>
              </div>
              <Tooltip title={item["When / how often"] || "No data available"} arrow>
                <IconButton>
                  <InfoIcon style={{ color: 'white' }} /> {/* White icon color */}
                </IconButton>
              </Tooltip>
            </TableCell>
          )}
          <TableCell>{renderEditableField(`${sectionKey}.recommendation.${sectionKey}.${index}.Explanation`, item["Explanation"])}</TableCell>
          <TableCell>{renderInfoButton(item, sectionKey)}</TableCell>
          <TableCell>
            <TextField
              type="number"
              label="Score"
              value={validation.score || ''}
              onChange={(e) => handleScoreChange(rowID, e.target.value)}
              disabled={!isEditing}
              fullWidth
              variant="outlined"
              size="small"
            />
          </TableCell>
          <TableCell>
            <TextField
              label="Comment"
              value={validation.comment || ''}
              onChange={(e) => handleCommentChange(rowID, e.target.value)}
              disabled={!isEditing}
              fullWidth
              variant="outlined"
              size="small"
            />
          </TableCell>
          <TableCell>{renderVerificationCheckbox(rowID)}</TableCell>
        </TableRow>
      );
    })
  );

  return (
    <div className="follow-up-care-plan-container">
      <Typography variant="h4" className="follow-up-care-plan-title">Follow-up Care Plan</Typography>
      <Grid container spacing={2}>
        {Object.keys(editedPlan).map((sectionKey) => (
          <Grid item xs={12} key={sectionKey}>
            <Card>
              <CardContent>
                <Typography variant="h6">{sectionKey}</Typography>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Visit Type</TableCell>
                      {sectionKey === "Cancer Surveillance or Other Recommended Tests" && (
                        <TableCell>Coordinating Provider</TableCell>
                      )}
                      <TableCell>When/How Often</TableCell>
                      <TableCell>Explanation</TableCell>
                      <TableCell>References</TableCell>
                      <TableCell>Score</TableCell>
                      <TableCell>Comment</TableCell>
                      <TableCell>Verified</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {editedPlan[sectionKey]?.recommendation?.[sectionKey] &&
                      renderSectionRows(editedPlan[sectionKey].recommendation[sectionKey], sectionKey)}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        ))}
        <Grid item xs={12}>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
            <Button variant="contained" color="primary" onClick={handleEditClick}>
              {isEditing ? 'Save' : 'Edit'}
            </Button>
          </div>
        </Grid>
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
