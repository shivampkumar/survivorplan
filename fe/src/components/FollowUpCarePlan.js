import React, { useState } from 'react';
import { Button, Card, CardContent, Grid, Table, TableBody, IconButton, TableCell, TableHead, TableRow, Typography, TextField, Tooltip } from '@mui/material';
import ReferencesDialog from './ReferencesDialog';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import InfoIcon from '@mui/icons-material/Info';
import './FollowUpCarePlan.css';

const FollowUpCarePlan = ({ followUpCarePlan }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedPlan, setEditedPlan] = useState(followUpCarePlan);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReferences, setCurrentReferences] = useState([]);
  const [verifiedRows, setVerifiedRows] = useState({});
  const [dateValues, setDateValues] = useState({}); 

  followUpCarePlan = followUpCarePlan['Follow Up Care Plan'];

  const handleOpenDialog = (fileNames, pageLabels, sectionKey) => {
    const sectionContext = followUpCarePlan[sectionKey]?.context || [];
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

  const handleVerificationChange = (path) => {
    setVerifiedRows((prevVerifiedRows) => ({
      ...prevVerifiedRows,
      [path]: !prevVerifiedRows[path],
    }));
  };

  const handleEditClick = () => {
    setIsEditing(!isEditing);
  };

  const handleChange = (path, value) => {
    const keys = path.split('.');
    const lastKey = keys.pop();
    const lastObj = keys.reduce((obj, key) => obj[key] = obj[key] || {}, editedPlan);
    lastObj[lastKey] = value;
    setEditedPlan({ ...editedPlan });
  };

  const handleDateChange = (path, newValue) => {
    setDateValues((prev) => ({
      ...prev,
      [path]: newValue,
    }));
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

  const renderInfoButton = (item, sectionKey) => (
    <Button onClick={() => handleOpenDialog(item["File names"], item["Page labels"], sectionKey)}>i</Button>
  );

  const renderVerificationRadio = (path) => (
    <input
      type="radio"
      checked={!!verifiedRows[path]}
      onChange={() => handleVerificationChange(path)}
    />
  );

  const renderSectionRows = (section, sectionKey) => (
    section.map((item, index) => {
      const rowClass = verifiedRows[`${sectionKey}.${index}`] ? 'table-row verified' : 'table-row';
      const lastVisitDate = '2024-01-15'; // Example last visit date
      const nextVisitDatePath = `visit.${index}.nextVisitDate`;
      const nextVisitDateStatic = '2024-06-15'; // Example next visit date
  
      return (
        <TableRow key={index} className={rowClass}>
          <TableCell>{renderEditableField(`${sectionKey}.${index}.Visit type`, item["Visit type"] || item["Test type"] || item["Treatment effect"] || item["Issue"] || item["Lifestyle"] || item["Resource"])}</TableCell>
          {sectionKey === "Cancer Surveillance or Other Recommended Tests" && (
            <TableCell>{renderEditableField(`${sectionKey}.${index}.Coordinating provider`, item["Coordinating provider"])}</TableCell>
          )}
          {"When / how often" in item && (
            <TableCell>
              <div>
                <Typography variant="body2">
                  Last Visit Date: {new Date(lastVisitDate).toLocaleDateString()}
                </Typography>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <DatePicker
                    label="Next Visit Date"
                    value={dateValues[nextVisitDatePath] || new Date(nextVisitDateStatic)}
                    onChange={(newValue) => handleDateChange(nextVisitDatePath, newValue)}
                    renderInput={(params) => <TextField {...params} variant="outlined" size="small" fullWidth />}
                  />
                </LocalizationProvider>
                <Tooltip title={item["When / how often"] || "No data available"} arrow>
                  <IconButton>
                    <InfoIcon />
                  </IconButton>
                </Tooltip>
              </div>
            </TableCell>
          )}
          <TableCell>{renderEditableField(`${sectionKey}.${index}.Explanation`, item["Explanation"])}</TableCell>
          <TableCell>{renderInfoButton(item, sectionKey)}</TableCell>
          <TableCell>{renderVerificationRadio(`${sectionKey}.${index}`)}</TableCell>
        </TableRow>
      );
    })
  );

  return (
    <div className="follow-up-care-plan-container">
      <Typography variant="h4" className="follow-up-care-plan-title">Follow-up Care Plan</Typography>
      <Grid container spacing={2} backgroundColor="#282828">
        {Object.keys(followUpCarePlan).filter(key => ['Schedule of Clinical Visits'].includes(key)).map((sectionKey) => (
          <Grid item xs={12} key={sectionKey}>
            <Card>
              <CardContent>
                <Typography variant="h6">{sectionKey}</Typography>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Visit Type</TableCell>
                      <TableCell>When/How Often</TableCell>
                      <TableCell>Explanation</TableCell>
                      <TableCell>References</TableCell>
                      <TableCell>Validate</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {renderSectionRows(followUpCarePlan[sectionKey].recommendation[sectionKey], sectionKey)}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        ))}
        {Object.keys(followUpCarePlan).filter(key => ['Cancer Surveillance or Other Recommended Tests'].includes(key)).map((sectionKey) => (
          <Grid item xs={12} key={sectionKey}>
            <Card>
              <CardContent>
                <Typography variant="h6">{sectionKey}</Typography>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Test Type</TableCell>
                      <TableCell>Coordinating Provider</TableCell>
                      <TableCell>When/How Often</TableCell>
                      <TableCell>Explanation</TableCell>
                      <TableCell>References</TableCell>
                      <TableCell>Validate</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {renderSectionRows(followUpCarePlan[sectionKey].recommendation[sectionKey], sectionKey)}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </Grid>
        ))}
        {Object.keys(followUpCarePlan).filter(key => ['Possible late and long-term effects of cancer treatment', 'Other issues', 'Lifestyle and behavior', 'Helpful resources'].includes(key)).map((sectionKey) => (
          <Grid item xs={12} key={sectionKey}>
            <Card>
              <CardContent>
                <Typography variant="h6">{sectionKey}</Typography>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Treatment Effect/Issue/Lifestyle/Resource</TableCell>
                      <TableCell>Explanation</TableCell>
                      <TableCell>References</TableCell>
                      <TableCell>Validate</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {renderSectionRows(followUpCarePlan[sectionKey].recommendation[sectionKey], sectionKey)}
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
