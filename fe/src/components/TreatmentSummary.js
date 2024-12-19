import React, { useState, useEffect } from 'react';
import PatientTextDialog from './PatientTextDialog';
import './TreatmentSummary.css'; // Ensure this file is updated with styles as needed
import { StaticDataService } from '../services/StaticDataService';
import { Typography } from '@mui/material';

const TreatmentSummary = ({ patientId }) => {
  const [treatmentData, setTreatmentData] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedSummary, setEditedSummary] = useState(null);
  const [patientDialogOpen, setPatientDialogOpen] = useState(false);
  const [verifiedRows, setVerifiedRows] = useState({});

  useEffect(() => {
    const loadData = async () => {
      const data = await StaticDataService.getPatientData(patientId);
      setTreatmentData(data.treatmentSummary);
    };
    loadData();
  }, [patientId]);

  useEffect(() => {
    setEditedSummary(treatmentData);
  }, [treatmentData]);

  const handleChange = (path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const lastObj = keys.reduce((obj, key) => obj[key] = obj[key] || {}, editedSummary);
    lastObj[lastKey] = value;
    setEditedSummary({ ...editedSummary });
  };

  const handleEditClick = () => {
    setIsEditing(!isEditing);
  };

  const handleOpenPatientTextDialog = () => {
    setPatientDialogOpen(true);
  };

  const handleVerificationChange = (path) => {
    setVerifiedRows((prevVerifiedRows) => ({
      ...prevVerifiedRows,
      [path]: !prevVerifiedRows[path],
    }));
    // TODO: Update verification status via API
  };

  const renderEditableField = (path, value) => (
    isEditing ? (
      <input
        type="text"
        value={value}
        onChange={(e) => handleChange(path, e.target.value)}
      />
    ) : (
      value
    )
  );

  const renderInfoButton = () => (
    <button onClick={handleOpenPatientTextDialog}>i</button>
  );

  const renderVerificationRadio = (path) => (
    <input
      type="radio"
      checked={!!verifiedRows[path]}
      onChange={() => handleVerificationChange(path)}
    />
  );

  const generateSectionRows = (section, sectionPath, keys) => {
    return keys.map((key) => {
      if (!(key in section)) {
        return null; // Skip missing keys
      }

      const value = section[key];
      const isObject = typeof value === 'object' && !Array.isArray(value) && value !== null;
      const rowClass = verifiedRows[`${sectionPath}.${key}`] ? 'table-row verified' : 'table-row';

      return (
        <div
          className={rowClass}
          key={`${sectionPath}.${key}`}
        >
          <div className="label">{key}:</div>
          <div className="value">
            {isObject ? renderSection(value, `${sectionPath}.${key}`, Object.keys(value)) : renderEditableField(`${sectionPath}.${key}`, value)}
          </div>
          <div className="info-button">{renderInfoButton()}</div>
          <div className="verification-radio">{renderVerificationRadio(`${sectionPath}.${key}`)}</div>
          <PatientTextDialog
            open={patientDialogOpen}
            onClose={() => setPatientDialogOpen(false)}
            patientText={treatmentData.patient_text}
          />
        </div>
      );
    }).filter(Boolean);
  };

  const renderSection = (sectionData, path, keys) => (
    <div className="section">
      {keys.map((sectionTitle, index) => (
        <React.Fragment key={index}>
          <h3 className="section-title">{sectionTitle}</h3>
          <div className="table">
            {generateSectionRows(sectionData[sectionTitle], `${path}.${sectionTitle}`, Object.keys(sectionData[sectionTitle]))}
          </div>
        </React.Fragment>
      ))}
    </div>
  );

  if (!treatmentData) return <div>Loading...</div>;

  return (
    <div className="card">
      <div className="treatment-summary">
        <Typography variant="h4" className="treatment-summary-title">
          Treatment Summary
        </Typography>

        <div className="section">
          <Typography variant="h6" className="section-title">Diagnosis</Typography>
          <div className="table">
            {Object.entries(treatmentData.Diagnosis).map(([key, value]) => (
              <div className="table-row" key={key}>
                <div className="label">{key}</div>
                <div className="value">{value || 'N/A'}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="section">
          <Typography variant="h6" className="section-title">Treatment Details</Typography>
          <div className="table">
            <div className="table-row">
              <div className="label">Surgery Conducted</div>
              <div className="value">{treatmentData.Surgery.conducted}</div>
            </div>
            {treatmentData.Surgery.conducted === 'Yes' && (
              <>
                <div className="table-row">
                  <div className="label">Surgery Procedure</div>
                  <div className="value">{treatmentData.Surgery.procedure || 'N/A'}</div>
                </div>
                {/* ... other surgery details */}
              </>
            )}
            
            <div className="table-row">
              <div className="label">Radiation Treatment</div>
              <div className="value">{treatmentData.RadiationTreatment.conducted}</div>
            </div>
            {/* ... radiation details if conducted */}

            <div className="table-row">
              <div className="label">Systemic Therapy</div>
              <div className="value">{treatmentData.SystemicTherapy.conducted}</div>
            </div>
            {treatmentData.SystemicTherapy.conducted === 'Yes' && 
              treatmentData.SystemicTherapy.agents.map((agent, index) => (
                <div className="table-row" key={index}>
                  <div className="label">Agent {index + 1}</div>
                  <div className="value">{agent.name} {agent.endDate ? `(End: ${agent.endDate})` : ''}</div>
                </div>
              ))
            }
          </div>
        </div>

        {/* Persistent Symptoms section */}
        {treatmentData.PersistentSymptoms.present === 'Yes' && (
          <div className="section">
            <Typography variant="h6" className="section-title">Persistent Symptoms</Typography>
            <div className="table">
              {treatmentData.PersistentSymptoms.symptoms.map((symptom, index) => (
                <div className="table-row" key={index}>
                  <div className="label">Symptom {index + 1}</div>
                  <div className="value">{symptom}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <button className="edit-button" onClick={handleEditClick}>
            {isEditing ? 'Save' : 'Edit'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TreatmentSummary;
