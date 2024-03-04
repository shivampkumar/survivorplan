import React, { useState, useEffect } from 'react';
import './TreatmentSummary.css'; // Ensure this file is updated with styles as needed

const TreatmentSummary = ({ summaryDetails, editMode, onEditChange }) => {
  const [editedSummary, setEditedSummary] = useState(summaryDetails);

  useEffect(() => {
    setEditedSummary(summaryDetails);
  }, [summaryDetails]);

  const handleChange = (path, value) => {
    // Allows for deep setting of values in the editedSummary state
    const keys = path.split('.');
    const lastKey = keys.pop();
    const lastObj = keys.reduce((obj, key) => obj[key] = obj[key] || {}, editedSummary);
    lastObj[lastKey] = value;
    setEditedSummary({ ...editedSummary });
  };

  const handleSave = () => {
    onEditChange(editedSummary);
  };

  const renderEditableField = (path, value) => (
    editMode ? (
      <input
        type="text"
        value={value}
        onChange={(e) => handleChange(path, e.target.value)}
      />
    ) : (
      value
    )
  );

  // Dynamically generate rows for each section
  const generateSectionRows = (section, sectionPath) => {
    if (Array.isArray(section)) {
      return section.map((item, index) => (
        <React.Fragment key={index}>
          {Object.entries(item).map(([key, value]) => (
            <div className="table-row" key={key}>
              <div className="label">{key}:</div>
              <div className="value">{renderEditableField(`${sectionPath}.${index}.${key}`, value)}</div>
            </div>
          ))}
        </React.Fragment>
      ));
    } else {
      return Object.entries(section).map(([key, value], index) => {
        const isObject = typeof value === 'object' && !Array.isArray(value) && value !== null;
        return (
          <div className="table-row" key={key}>
            <div className="label">{key}:</div>
            <div className="value">
              {isObject ? renderSection(value, `${sectionPath}.${key}`) : renderEditableField(`${sectionPath}.${key}`, value)}
            </div>
          </div>
        );
      });
    }
  };

  const renderSection = (sectionData, path) => (
    <div className="section">
      {Object.entries(sectionData).map(([sectionTitle, section], index) => (
        <React.Fragment key={index}>
          <h3 className="section-title">{sectionTitle}</h3>
          <div className="table">
            {generateSectionRows(section, `${path}.${sectionTitle}`)}
          </div>
        </React.Fragment>
      ))}
    </div>
  );

  return (
    <div className="card">
      <div className="treatment-summary">
        <h2 className="treatment-summary-title">Treatment Summary</h2>
        {renderSection(editedSummary['Treatment Summary'], 'Treatment Summary')}
        {editMode && <button className="save-button" onClick={handleSave}>Save</button>}
      </div>
    </div>
  );
};

export default TreatmentSummary;
