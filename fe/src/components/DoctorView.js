import React, { useState, useEffect } from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';
import FollowUpCarePlan from './FollowUpCarePlan';
import PatientSidebar from './PatientSidebar';
import { Box, Divider, Tab, Tabs, Typography, Button, Menu, MenuItem } from '@mui/material';
import DoctorHome from './DoctorHome';
import { StaticDataService } from '../services/StaticDataService';
import './LoadingAnimation.css';

const DoctorView = () => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientDetails, setPatientDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState(0);
  const [anchorEl, setAnchorEl] = useState(null);

  useEffect(() => {
    const loadPatients = async () => {
      try {
        const allPatients = await StaticDataService.getAllPatients();
        setPatients(allPatients);
        setLoading(false);
      } catch (error) {
        console.error('Error loading patients:', error);
        setLoading(false);
      }
    };
    loadPatients();
  }, []);

  useEffect(() => {
    const loadPatientDetails = async () => {
      if (selectedPatient !== null) {
        try {
          const details = await StaticDataService.getPatientData(selectedPatient);
          setPatientDetails(details);
        } catch (error) {
          console.error('Error loading patient details:', error);
        }
      }
    };
    loadPatientDetails();
  }, [selectedPatient]);

  const handleChangeTab = (event, newValue) => {
    setSelectedTab(newValue);
  };

  const handlePatientSelect = (patientId) => {
    console.log('Selected patient:', patientId);
    setSelectedPatient(patientId);
  };

  const handleExportClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const downloadPdf = () => {
    if (!selectedPatient) return;
    // For now, just show an alert since we're using static data
    alert('PDF download functionality disabled in static mode');
    handleMenuClose();
  };

  const exportToEpic = () => {
    if (!selectedPatient) return;
    // For now, just show an alert since we're using static data
    alert('EPIC export functionality disabled in static mode');
    handleMenuClose();
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ flexGrow: 1, backgroundColor: '#1E1E1E', color: '#FFFFFF', minHeight: '100vh' }}>
      <Box sx={{ borderBottom: 1, borderColor: '#282828' }}>
        <Tabs value={selectedTab} onChange={handleChangeTab} aria-label="doctor view tabs" textColor="inherit">
          <Tab label="Home" />
          <Tab label="Existing patient directory" />
          <Tab label="Add new patients" />
          <Tab label="Clinical Guideline" />
        </Tabs>
      </Box>

      {selectedTab === 0 && (
        <Box p={3}>
          <DoctorHome />
        </Box>
      )}

      {selectedTab === 1 && (
        <Box display="flex" width="100%">
          <PatientSidebar 
            patients={patients}
            onSelectPatient={handlePatientSelect}
            selectedPatientId={selectedPatient}
          />
          <Divider orientation="vertical" flexItem sx={{ backgroundColor: '#282828' }} />
          <Box flex={1} padding="20px" backgroundColor="#282828">
            {selectedPatient ? (
              <>
                {patientDetails ? (
                  <>
                    <Box mb={3}>
                      <PatientInfo patientDetails={patientDetails.General_Information} />
                    </Box>
                    <Box mb={3}>
                      <TreatmentSummary data={patientDetails.Treatment_Summary} />
                    </Box>
                    <Box mb={3}>
                      <FollowUpCarePlan data={patientDetails.Follow_Up_Care_Plan} />
                    </Box>
                    <Box display="flex" justifyContent="flex-end">
                      <Button
                        variant="contained"
                        color="primary"
                        onClick={handleExportClick}
                      >
                        Export Care Plan
                      </Button>
                      <Menu
                        anchorEl={anchorEl}
                        open={Boolean(anchorEl)}
                        onClose={handleMenuClose}
                      >
                        <MenuItem onClick={downloadPdf}>Download as PDF</MenuItem>
                        <MenuItem onClick={exportToEpic}>Save to EPIC</MenuItem>
                      </Menu>
                    </Box>
                  </>
                ) : (
                  <Box className="loading-container" sx={{ textAlign: 'center', mt: 5 }}>
                    <Typography variant="h6" className="loading-text">
                      Loading patient details
                      <span className="loading-dots">...</span>
                    </Typography>
                  </Box>
                )}
              </>
            ) : (
              <Typography>Select a patient to view details</Typography>
            )}
          </Box>
        </Box>
      )}

      {selectedTab === 2 && (
        <Box p={3}>
          {/* Content for the Add new patients tab */}
        </Box>
      )}

      {selectedTab === 3 && (
        <Box p={3}>
          {/* Content for the Clinical Guideline tab */}
        </Box>
      )}
    </Box>
  );
};

export default DoctorView;
