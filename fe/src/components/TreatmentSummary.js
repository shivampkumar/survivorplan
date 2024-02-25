import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import EditableField from './EditableField'; // Ensure this component can handle various data types

// Helper function to render nested data
const renderNestedData = (data, editMode, onEditChange, basePath = '') => {
  if (Array.isArray(data)) {
    return data.map((item, index) => (
      <div key={index}>
        {typeof item === 'object' ? renderNestedData(item, editMode, onEditChange, `${basePath}[${index}]`) : (
          <EditableField
            field={`${basePath}[${index}]`}
            value={item}
            editMode={editMode}
            onChange={(newValue) => onEditChange(`${basePath}[${index}]`, newValue)}
          />
        )}
      </div>
    ));
  } else if (typeof data === 'object') {
    return Object.entries(data).map(([key, value]) => (
      <div key={key}>
        <Typography variant="subtitle1">{key}</Typography>
        {typeof value === 'object' ? renderNestedData(value, editMode, onEditChange, `${basePath}.${key}`) : (
          <EditableField
            field={`${basePath}.${key}`}
            value={value}
            editMode={editMode}
            onChange={(newValue) => onEditChange(`${basePath}.${key}`, newValue)}
          />
        )}
      </div>
    ));
  } else {
    // For primitive values that shouldn't exist at this level
    return null;
  }
};

const TreatmentSummary = ({ summaryDetails, editMode, onEditChange }) => {
  return (
    <Card variant="outlined">
      <CardContent>
        <Typography variant="h5" gutterBottom>Treatment Summary</Typography>
        {/* Render nested data */}
        {renderNestedData(summaryDetails, editMode, onEditChange)}
      </CardContent>
    </Card>
  );
};

export default TreatmentSummary;
