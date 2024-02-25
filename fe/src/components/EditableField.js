import React from 'react';
import { TextField } from '@mui/material';

const EditableField = ({ field, value, editMode, onChange }) => {
  if (editMode) {
    return (
      <TextField
        label={field}
        defaultValue={typeof value === 'object' ? JSON.stringify(value) : value}
        onChange={(e) => onChange(field, e.target.value)}
        fullWidth
      />
    );
  }

  return (
    <p>{`${field}: ${typeof value === 'object' ? JSON.stringify(value) : value}`}</p>
  );
};

export default EditableField;
