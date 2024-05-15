import React, { useState, useEffect } from 'react';
import PatientTextDialog from './PatientTextDialog';
import './TreatmentSummary.css'; // Ensure this file is updated with styles as needed

const TreatmentSummary = ({ summaryDetails, patient_text, onEditChange }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedSummary, setEditedSummary] = useState(summaryDetails);
  const [patientDialogOpen, setPatientDialogOpen] = useState(false);
  const [verifiedRows, setVerifiedRows] = useState({});

  const hardcodedKeys = {
    "Treatment Summary": {
      "Diagnosis": ["Cancer type", "Diagnosis Date", "Cancer stage"],
      "Treatment Completed": ["Surgery", "Surgery Date(s) (year)", "Surgical Procedure/location/findings", "Radiation", "Body area treated", "End Date (year)", "Systemic Therapy (Chemotherapy, hormonal therapy, other)"],
      "Names of Agents used in Completed Treatments": ["Agent 1", "Agent 2", "Agent 3"],
      "Persistent symptoms or side effects at completion of treatment": ["Symptoms of side effects", "Symptom or side effect types"],
      "Treatment Ongoing and Side Effects": ["Need for ongoing (adjuvant) treatment for cancer", "Ongoing treatment 1"]
    }
  };

  useEffect(() => {
    setEditedSummary(summaryDetails);
  }, [summaryDetails]);

  const handleChange = (path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const lastObj = keys.reduce((obj, key) => obj[key] = obj[key] || {}, editedSummary);
    lastObj[lastKey] = value;
    setEditedSummary({ ...editedSummary });
  };

  const handleSave = () => {
    onEditChange(editedSummary);
    setIsEditing(false);
    // TODO: Save changes via API
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
            patientText={patient_text}
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
            {generateSectionRows(sectionData[sectionTitle], `${path}.${sectionTitle}`, hardcodedKeys["Treatment Summary"][sectionTitle] || Object.keys(sectionData[sectionTitle]))}
          </div>
        </React.Fragment>
      ))}
    </div>
  );

  return (
    <div className="card">
      <div className="treatment-summary">
        <h2 className="treatment-summary-title">Treatment Summary</h2>
        {renderSection(editedSummary['Treatment Summary'], 'Treatment Summary', Object.keys(hardcodedKeys["Treatment Summary"]))}
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
