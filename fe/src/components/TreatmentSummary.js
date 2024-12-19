// TreatmentSummary.js
import React, { useState, useEffect } from 'react';
import PatientTextDialog from './PatientTextDialog';
import axios from 'axios';
import { TextField, Button, Checkbox, Typography } from '@mui/material';
import './TreatmentSummary.css';

const API_BASE_URL = 'http://20.168.8.23:8080/api';

// Function to generate consistent row IDs
const generateRowID = (sectionKey, key) => {
  const content = `${sectionKey}-${key}`;
  let hash = 0;
  if (content.length === 0) return hash.toString();
  for (let i = 0; i < content.length; i++) {
    const char = content.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // Convert to 32bit integer
  }
  return `TS-${hash.toString()}`;
};

const TreatmentSummary = ({ summaryDetails, validations, patientID, patient_text }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedSummary, setEditedSummary] = useState(summaryDetails['Treatment Summary'] || {});
  const [patientDialogOpen, setPatientDialogOpen] = useState(false);
  const [verifiedRows, setVerifiedRows] = useState({});
  const [validationData, setValidationData] = useState({});

  // Hardcoded keys to render sections
  const hardcodedKeys = {
    "Diagnosis": ["Cancer type", "Diagnosis Date", "Cancer stage"],
    "Treatment Completed": ["Surgery", "Surgery Date(s) (year)", "Surgical Procedure/location/findings", "Radiation", "Body area treated", "End Date (year)", "Systemic Therapy (Chemotherapy, hormonal therapy, other)"],
    "Names of Agents used in Completed Treatments": ["Agent 1", "Agent 2", "Agent 3"],
    "Persistent symptoms or side effects at completion of treatment": ["Symptoms of side effects", "Symptom or side effect types"],
    "Treatment Ongoing and Side Effects": ["Need for ongoing (adjuvant) treatment for cancer", "Ongoing treatment 1"]
  };

  // Load validation data when component mounts
  useEffect(() => {
    if (validations) {
      setValidationData(validations);
      const initialVerifiedRows = {};
      for (const rowID in validations) {
        initialVerifiedRows[rowID] = validations[rowID].verified;
      }
      setVerifiedRows(initialVerifiedRows);
    }
  }, [validations]);

  const handleChange = (path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const lastObj = keys.reduce((obj, key) => obj[key], editedSummary);
    lastObj[lastKey] = value;
    setEditedSummary({ ...editedSummary });
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

  const handleVerificationChange = (rowID) => {
    setVerifiedRows((prevVerifiedRows) => ({
      ...prevVerifiedRows,
      [rowID]: !prevVerifiedRows[rowID],
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

  const handleEditClick = () => {
    if (isEditing) {
      handleSaveValidations();
    }
    setIsEditing(!isEditing);
  };

  const handleOpenPatientTextDialog = () => {
    setPatientDialogOpen(true);
  };

  const renderEditableField = (path, value) => (
    isEditing ? (
      <TextField
        value={value}
        onChange={(e) => handleChange(path, e.target.value)}
        fullWidth
        variant="outlined"
        size="small"
        style={{ color: '#FFFFFF' }}
        InputProps={{
          style: { color: '#FFFFFF' },
        }}
      />
    ) : (
      <Typography variant="body2">{value}</Typography>
    )
  );

  const renderScoreField = (rowID) => (
    <TextField
      type="number"
      label="Score"
      value={validationData[rowID]?.score || ''}
      onChange={(e) => handleScoreChange(rowID, e.target.value)}
      disabled={!isEditing}
      fullWidth
      variant="outlined"
      size="small"
      style={{ color: '#FFFFFF' }}
      InputProps={{
        style: { color: '#FFFFFF' },
      }}
    />
  );

  const renderCommentField = (rowID) => (
    <TextField
      label="Comment"
      value={validationData[rowID]?.comment || ''}
      onChange={(e) => handleCommentChange(rowID, e.target.value)}
      disabled={!isEditing}
      fullWidth
      variant="outlined"
      size="small"
      style={{ color: '#FFFFFF' }}
      InputProps={{
        style: { color: '#FFFFFF' },
      }}
    />
  );

  const renderVerificationCheckbox = (rowID) => (
    <Checkbox
      checked={!!verifiedRows[rowID]}
      onChange={() => handleVerificationChange(rowID)}
      disabled={!isEditing}
      style={{ color: '#FFFFFF' }}
    />
  );

  const generateSectionRows = (sectionData, sectionKey) => {
    const keys = hardcodedKeys[sectionKey] || Object.keys(sectionData);
    return keys.map((key) => {
      if (!(key in sectionData)) {
        return null; // Skip missing keys
      }

      const value = sectionData[key];
      const rowID = generateRowID(sectionKey, key);

      return (
        <div className="table-row" key={rowID}>
          <div className="label">{key}:</div>
          <div className="value">{renderEditableField(`${sectionKey}.${key}`, value)}</div>
          <div className="score-field">{renderScoreField(rowID)}</div>
          <div className="comment-field">{renderCommentField(rowID)}</div>
          <div className="verification-checkbox">{renderVerificationCheckbox(rowID)}</div>
        </div>
      );
    }).filter(Boolean);
  };

  const renderSection = (sectionData) => (
    Object.keys(hardcodedKeys).map((sectionKey) => (
      <div className="section" key={sectionKey}>
        <h3 className="section-title">{sectionKey}</h3>
        <div className="table">
          {generateSectionRows(sectionData[sectionKey], sectionKey)}
        </div>
      </div>
    ))
  );

  return (
    <div className="card">
      <div className="treatment-summary">
        <h2 className="treatment-summary-title">Treatment Summary</h2>
        {renderSection(editedSummary)}
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <Button variant="contained" color="primary" onClick={handleEditClick}>
            {isEditing ? 'Save' : 'Edit'}
          </Button>
        </div>
      </div>
      <PatientTextDialog
        open={patientDialogOpen}
        onClose={() => setPatientDialogOpen(false)}
        patientText={patient_text}
      />
    </div>
  );
};

export default TreatmentSummary;
