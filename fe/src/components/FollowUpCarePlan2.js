import React, { useState } from 'react';
import { Button, Card, CardContent, Dialog, DialogActions, DialogContent, DialogTitle, Typography, Grid } from '@mui/material';
import EditableField from './EditableField'; // Assuming this is the path to your EditableField component

const FollowUpCarePlan2 = ({ followUpCarePlan, editMode, onEditChange }) => {
    const [openDialog, setOpenDialog] = useState(false);
    const [dialogContent, setDialogContent] = useState([]);

    const handleOpenDialog = (contextData) => {
        // Assuming contextData is an array of { metadata, text } objects
        const content = contextData.map((context, index) => (
            <Typography key={index}>{context.text}</Typography>
        ));
        setDialogContent(content);
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
    };

    return (
        <Grid container spacing={2}>
            {Object.entries(followUpCarePlan).map(([key, value], sectionIndex) => {
                if (key === 'cancer_type' || key === 'patient_data' || key === 'context') {
                    // Directly render editable fields for cancer_type and patient_data if in editMode
                    if (editMode && (key === 'cancer_type' || key === 'patient_data')) {
                        return (
                            <EditableField
                                key={key}
                                field={key}
                                value={value}
                                editMode={editMode}
                                onChange={(newValue) => onEditChange(key, newValue)}
                            />
                        );
                    }
                    return null;
                }

                return (
                    <Grid item xs={12} key={sectionIndex}>
                        <Card variant="outlined">
                            <CardContent>
                                <Typography variant="h6" gutterBottom>{key.replace(/_/g, ' ')}</Typography>
                                {value.recommendation && Object.entries(value.recommendation).map(([subKey, items], itemIndex) => (
                                    <div key={itemIndex}>
                                        <Typography variant="subtitle1">{subKey}</Typography>
                                        {items.map((item, detailIndex) => (
                                            <div key={detailIndex}>
                                                {Object.entries(item).map(([itemKey, itemValue], entryIndex) => (
                                                    editMode && itemKey !== 'File names' && itemKey !== 'Page labels' ? (
                                                        <EditableField
                                                            key={`${itemKey}-${entryIndex}`}
                                                            field={itemKey}
                                                            value={itemValue}
                                                            editMode={editMode}
                                                            onChange={(newValue) => onEditChange(`${key}.${subKey}.${itemKey}`, newValue, detailIndex)}
                                                        />
                                                    ) : (
                                                        <Typography key={itemKey}>{`${itemKey}: ${itemValue}`}</Typography>
                                                    )
                                                ))}
                                                <Button
                                                    onClick={() => handleOpenDialog(value.context)}
                                                    variant="contained"
                                                    size="small"
                                                    style={{ marginTop: '8px', marginBottom: '8px' }}
                                                >
                                                    Show References
                                                </Button>
                                            </div>
                                        ))}
                                    </div>
                                ))}
                            </CardContent>
                        </Card>
                    </Grid>
                );
            })}

            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="lg" fullWidth>
                <DialogTitle>Reference Details</DialogTitle>
                <DialogContent dividers>
                    {dialogContent}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Close</Button>
                </DialogActions>
            </Dialog>
        </Grid>
    );
};