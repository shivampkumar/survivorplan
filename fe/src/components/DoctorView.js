import React, { useState, useEffect, useRef } from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';
import FollowUpCarePlan from './FollowUpCarePlan';
import PatientSidebar from './PatientSidebar'; // Import the sidebar
import { Box, Divider, Tab, Tabs } from '@mui/material';
import DoctorHome from './DoctorHome';
import axios from 'axios';

const API_BASE_URL = 'http://20.168.8.23:8080/api';

const DoctorView = ({ patients }) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [selectedPatient, setSelectedPatient] = useState(null); // Track selected patient
  const [patientDetails, setPatientDetails] = useState(null); // New state for patient details
  const [taskId, setTaskId] = useState(null); // State to track task ID
  const [taskStatus, setTaskStatus] = useState(null); // State to track task status
  const pollingRef = useRef(null); // To store the polling interval

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
            setPatientDetails(response.data); // Set patient details for the selected patient
          }
        })
        .catch(error => console.error("Failed to fetch patient details", error));
    }
  }, [selectedPatient]);

  const pollTaskStatus = (taskId) => {
    const pollInterval = 2000; // Poll every 2 seconds

    const checkStatus = () => {
      axios.get(`${API_BASE_URL}/status/${taskId}`)
        .then(response => {
          const taskState = response.data.state;

          if (taskState === 'SUCCESS') {
            setPatientDetails(response.data.result); // Assuming the task result contains the updated patient details
            alert('Plan generated successfully');
            clearInterval(pollingRef.current); // Stop polling
          } else if (taskState === 'FAILURE') {
            alert('Failed to generate plan');
            clearInterval(pollingRef.current); // Stop polling
          } else {
            setTaskStatus(taskState);
          }
        })
        .catch(error => {
          console.error("Failed to check task status", error);
        });
    };

    // Start the first status check
    if (pollingRef.current) {
      clearInterval(pollingRef.current); // Clear any existing interval
    }
    pollingRef.current = setInterval(checkStatus, pollInterval);
  };

  const onSelectPatient = (patient) => {
    setSelectedPatient(patient);
    setPatientDetails(null); // Reset patient details when a new patient is selected
    setTaskId(null); // Reset task ID
    setTaskStatus(null); // Reset task status
    if (pollingRef.current) {
      clearInterval(pollingRef.current); // Stop any ongoing polling
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={selectedTab} onChange={handleChangeTab} aria-label="doctor view tabs">
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
          <Divider orientation="vertical" flexItem />

          <Box flex={1} padding="20px">
            {selectedPatient ? (
              <>
                {patientDetails ? (
                  <>
                    <PatientInfo patientDetails={patientDetails['General Information']} />
                    <TreatmentSummary
                      summaryDetails={patientDetails}
                      patient_text={patientDetails['Relevant_patient_text']}
                    />
                    <FollowUpCarePlan
                      followUpCarePlan={patientDetails}
                    />
                  </>
                ) : (
                  <div>Loading patient details...</div>
                )}
              </>
            ) : (
              <div>Select a patient to view details</div>
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
