import React, { useState, useEffect, useRef } from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';
import FollowUpCarePlan from './FollowUpCarePlan';
import PatientSidebar from './PatientSidebar';
import { Box, Divider, Tab, Tabs, Typography, Button, Menu, MenuItem } from '@mui/material'; // Import necessary MUI components
import DoctorHome from './DoctorHome';
import axios from 'axios';
import './LoadingAnimation.css'; // Import the CSS for the loading animation

const API_BASE_URL = 'http://20.168.8.23:8080/api';

const DoctorView = ({ patients }) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientDetails, setPatientDetails] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const pollingRef = useRef(null);

  const [anchorEl, setAnchorEl] = useState(null);

  const handleChangeTab = (event, newValue) => {
    setSelectedTab(newValue);
  };

  useEffect(() => {
    if (selectedPatient) {
      axios.get(`${API_BASE_URL}/patients/${selectedPatient.patientID}`)
        .then(response => {
          if (response.status === 202) {
            const taskId = response.data.task_id;
            setTaskId(taskId);
            pollTaskStatus(taskId);
          } else {
            setPatientDetails(response.data);
          }
        })
        .catch(error => console.error("Failed to fetch patient details", error));
    }
  }, [selectedPatient]);

  const pollTaskStatus = (taskId) => {
    const pollInterval = 2000;

    const checkStatus = () => {
      axios.get(`${API_BASE_URL}/status/${taskId}`)
        .then(response => {
          const taskState = response.data.state;

          if (taskState === 'SUCCESS') {
            setPatientDetails(response.data.result);
            alert('Plan generated successfully');
            clearInterval(pollingRef.current);
          } else if (taskState === 'FAILURE') {
            alert('Failed to generate plan');
            clearInterval(pollingRef.current);
          } else {
            setTaskStatus(taskState);
          }
        })
        .catch(error => {
          console.error("Failed to check task status", error);
        });
    };

    if (pollingRef.current) {
      clearInterval(pollingRef.current);
    }
    pollingRef.current = setInterval(checkStatus, pollInterval);
  };

  const onSelectPatient = (patient) => {
    setSelectedPatient(patient);
    setPatientDetails(null);
    setTaskId(null);
    setTaskStatus(null);
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
    }
  };

  const handleExportClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const downloadPdf = () => {
    if (!selectedPatient) return;

    axios.get(`${API_BASE_URL}/generate_pdf/${selectedPatient.patientID}`, { responseType: 'blob' })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `CarePlan_${selectedPatient.patientID}.pdf`);
        document.body.appendChild(link);
        link.click();
      })
      .catch(error => {
        console.error("Failed to generate PDF", error);
      });

    handleMenuClose();
  };

  const exportToEpic = () => {
    if (!selectedPatient) return;

    axios.post(`${API_BASE_URL}/export_to_epic`, { patientID: selectedPatient.patientID })
      .then(response => {
        alert('Patient data exported to EPIC successfully');
      })
      .catch(error => {
        console.error("Failed to export patient data to EPIC", error);
        alert('Failed to export data to EPIC');
      });

    handleMenuClose();
  };

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
          <PatientSidebar patients={patients} onSelectPatient={onSelectPatient} />
          <Divider orientation="vertical" flexItem sx={{ backgroundColor: '#282828' }} />
          <Box flex={1} padding="20px" backgroundColor="#282828">
            {selectedPatient ? (
              <>
                {patientDetails ? (
                  <>
                    <Box mb={3}>
                      <PatientInfo patientDetails={patientDetails['General Information']} />
                    </Box>
                    <Box mb={3}>
                      <TreatmentSummary
                        summaryDetails={patientDetails}
                        patient_text={patientDetails['Relevant_patient_text']}
                      />
                    </Box>
                    <Box mb={3}>
                      <FollowUpCarePlan followUpCarePlan={patientDetails} />
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
                    <Typography variant="body2" className="loading-text-secondary">
                      Please wait while we retrieve the information.
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
