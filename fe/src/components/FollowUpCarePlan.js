import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, Grid, Table, TableBody, IconButton, TableCell, TableHead, TableRow, Typography, TextField, Tooltip, Checkbox } from '@mui/material';
import ReferencesDialog from './ReferencesDialog';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import InfoIcon from '@mui/icons-material/Info';
import './FollowUpCarePlan.css';
import { StaticDataService } from '../services/StaticDataService';

const FollowUpCarePlan = ({ patientId }) => {
  const [followUpData, setFollowUpData] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedPlan, setEditedPlan] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentReferences, setCurrentReferences] = useState([]);
  const [verifiedRows, setVerifiedRows] = useState({});
  const [dateValues, setDateValues] = useState({}); 

  useEffect(() => {
    const loadData = async () => {
      const data = await StaticDataService.getPatientData(patientId);
      setFollowUpData(data.followUpCarePlan);
    };
    loadData();
  }, [patientId]);

  const handleOpenDialog = (fileNames, pageLabels, sectionKey) => {
    const sectionContext = followUpData[sectionKey]?.context || [];
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

  const renderSectionRows = (items, sectionKey) => {
    return items.map((item, index) => (
      <TableRow key={index}>
        {sectionKey === 'Cancer Surveillance or Other Recommended Tests' ? (
          <>
            <TableCell>{item['Test type']}</TableCell>
            <TableCell>{item['When / how often']}</TableCell>
            <TableCell>{item['Explanation']}</TableCell>
            <TableCell>Context ID: {item['Retrieved context id']}</TableCell>
            <TableCell>
              <Checkbox />
            </TableCell>
          </>
        ) : (
          <>
            <TableCell>{item['Lifestyle'] || item['Issue'] || item['Resource']}</TableCell>
            <TableCell>{item['Explanation']}</TableCell>
            <TableCell>Context ID: {item['Retrieved context id']}</TableCell>
            <TableCell>
              <Checkbox />
            </TableCell>
          </>
        )}
      </TableRow>
    ));
  };

  if (!followUpData) return <div>Loading...</div>;

  return (
    <div className="follow-up-care-plan-container">
      <Typography variant="h4" className="follow-up-care-plan-title">
        Follow-up Care Plan
      </Typography>
      
      {Object.entries(followUpData).map(([sectionKey, section]) => (
        <Card key={sectionKey} className="section-card">
          <CardContent>
            <Typography variant="h6">{sectionKey}</Typography>
            <Table>
              <TableHead>
                <TableRow>
                  {sectionKey === 'Cancer Surveillance or Other Recommended Tests' ? (
                    <>
                      <TableCell>Test Type</TableCell>
                      <TableCell>When/How Often</TableCell>
                      <TableCell>Explanation</TableCell>
                      <TableCell>References</TableCell>
                      <TableCell>Validate</TableCell>
                    </>
                  ) : (
                    <>
                      <TableCell>Description</TableCell>
                      <TableCell>Explanation</TableCell>
                      <TableCell>References</TableCell>
                      <TableCell>Validate</TableCell>
                    </>
                  )}
                </TableRow>
              </TableHead>
              <TableBody>
                {renderSectionRows(section.recommendation[sectionKey], sectionKey)}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default FollowUpCarePlan;
