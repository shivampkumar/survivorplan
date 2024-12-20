import React, { useState } from 'react';
import PatientTextDialog from './PatientTextDialog';
import './TreatmentSummary.css';
import { Typography } from '@mui/material';

const TreatmentSummary = ({ data }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [patientDialogOpen, setPatientDialogOpen] = useState(false);
  const [verifiedRows, setVerifiedRows] = useState({});

  if (!data) return <div>Loading...</div>;

  const handleOpenPatientTextDialog = () => {
    setPatientDialogOpen(true);
  };

  const handleVerificationChange = (path) => {
    setVerifiedRows((prevVerifiedRows) => ({
      ...prevVerifiedRows,
      [path]: !prevVerifiedRows[path],
    }));
  };

  const renderInfoButton = () => (
    <button className="info-button" onClick={handleOpenPatientTextDialog}>
      i
    </button>
  );

  const renderVerificationRadio = (path) => (
    <input
      type="checkbox"
      checked={verifiedRows[path] || false}
      onChange={() => handleVerificationChange(path)}
    />
  );

  const renderSection = (title, data) => {
    if (!data) return null;

    // Handle array data (like Agents Used in Completed Treatments)
    if (Array.isArray(data)) {
      return (
        <div className="section">
          <Typography variant="h6" className="section-title">{title}</Typography>
          <div className="table">
            {data.map((item, index) => (
              <div key={index}>
                {Object.entries(item).map(([key, value]) => (
                  <div 
                    className={`table-row ${verifiedRows[`${title}.${key}`] ? 'verified' : 'unverified'}`} 
                    key={key}
                  >
                    <div className="label">{key}:</div>
                    <div className="value">{value}</div>
                    <div className="info-button">{renderInfoButton()}</div>
                    <div className="verification-radio">
                      {renderVerificationRadio(`${title}.${key}`)}
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      );
    }

    // Handle object data
    return (
      <div className="section">
        <Typography variant="h6" className="section-title">{title}</Typography>
        <div className="table">
          {Object.entries(data).map(([key, value]) => (
            <div 
              className={`table-row ${verifiedRows[`${title}.${key}`] ? 'verified' : 'unverified'}`} 
              key={key}
            >
              <div className="label">{key}:</div>
              <div className="value">{value}</div>
              <div className="info-button">{renderInfoButton()}</div>
              <div className="verification-radio">
                {renderVerificationRadio(`${title}.${key}`)}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="card">
      <div className="treatment-summary">
        <Typography variant="h4" className="treatment-summary-title">
          Treatment Summary
        </Typography>

        {/* Render Diagnosis Section */}
        {renderSection("Diagnosis", data.Diagnosis)}

        {/* Render Surgery Information */}
        {renderSection("Surgery Information", data["Surgery Information"])}

        {/* Render Radiation Treatment Information */}
        {renderSection("Radiation Treatment Information", data["Radiation Treatment Information"])}

        {/* Render Systemic Therapy Information */}
        {renderSection("Agents Used in Completed Treatments", data["Agents Used in Completed Treatments"])}

        {/* Render Symptoms Section */}
        {renderSection("Symptoms or Side Effects", data["Symptoms or Side Effects"])}

        {/* Render Ongoing Treatment Information */}
        {renderSection("Ongoing Treatment Information", data["Ongoing Treatment Information"])}

        {/* Additional Comments Section */}
        {data["Additional Comments"] && (
          <div className="section">
            <Typography variant="h6" className="section-title">Additional Comments</Typography>
            <div className="table">
              <div className="table-row">
                <div className="value">{data["Additional Comments"]}</div>
              </div>
            </div>
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
          <button className="edit-button" onClick={() => setIsEditing(!isEditing)}>
            {isEditing ? 'Save' : 'Edit'}
          </button>
        </div>

        <PatientTextDialog
          open={patientDialogOpen}
          onClose={() => setPatientDialogOpen(false)}
          patientText={data["Additional Comments"]}
        />
      </div>
    </div>
  );
};

export default TreatmentSummary;
