import React, { useState, useEffect } from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';
import FollowUpCarePlan from './FollowUpCarePlan';
import PatientSidebar from './PatientSidebar'; // Import the sidebar
import {Button, Box, Divider, Tab, Tabs } from '@mui/material';
import DoctorHome from './DoctorHome';
import axios from 'axios';

const API_BASE_URL = 'http://20.168.8.23:8080/api';

const DoctorView = ({ patients }) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [editMode, setEditMode] = useState(false);
  const [editedDetails, setEditedDetails] = useState({});
  const [selectedPatient, setSelectedPatient] = useState(null); // Track selected patient
  const [patientDetails, setPatientDetails] = useState(null); // New state for patient details

  const handleChangeTab = (event, newValue) => {
    setSelectedTab(newValue);
  };
  
  useEffect(() => {
    if (selectedPatient) {
      console.log(selectedPatient);
      axios.get(`${API_BASE_URL}/patients/${selectedPatient.patientID}`)
        .then(response => {
          setPatientDetails(response.data); // Set patient details for the selected patient
        })
        .catch(error => console.error("Failed to fetch patient details", error));
    }
  }, [selectedPatient]);

  const handleEditChange = (field, value) => {
    setEditedDetails(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async (editedSummary) => {
    const url = 'YOUR_API_ENDPOINT'; // Replace with your actual endpoint
    try {
      const response = await fetch(url, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedSummary),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      // Handle response data as needed
      console.log('Save successful', await response.json());
    } catch (error) {
      console.error('Failed to save changes:', error);
    }
  };
  

  const onSaveChanges = (editedDetails) => {
    if (selectedPatient) {
      axios.put(`${API_BASE_URL}/patients/${selectedPatient.id}`, editedDetails)
        .then(() => {
          alert('Changes saved successfully');
          // Optionally refresh patient details here
        })
        .catch(error => console.error("Failed to save changes", error));
    }
  };

  const onGeneratePlan = () => {
    if (selectedPatient) {
      axios.post(`${API_BASE_URL}/generate/${selectedPatient.id}`)
        .then(response => {
          setPatientDetails(response.data); // Assuming the API returns the updated patient details
          alert('Plan generated successfully');
        })
        .catch(error => console.error("Failed to generate plan", error));
    }
  };

  const toggleEditMode = () => {
    setEditMode(!editMode);
  };

  const onSelectPatient = (patient) => {
    setSelectedPatient(patient);
  };

  // Example layout with sidebar and main content
  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header and Tabs Menu */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider'}}>
        <Tabs value={selectedTab} onChange={handleChangeTab} aria-label="doctor view tabs">
          <Tab label="Home" />
          <Tab label="Existing patient directory" />
          <Tab label="Add new patients" />
          <Tab label="Clinical Guideline" />
        </Tabs>
      </Box>

      {/* Content for each tab */}
      {selectedTab === 0 && (
        <Box p={3}>
          <DoctorHome />
        </Box>
      )}

      {selectedTab === 1 && (
        <Box display="flex" width="100%">
          {/* Sidebar for selecting patients */}
          <PatientSidebar patients={patients} onSelectPatient={onSelectPatient} />
          <Divider orientation="vertical" flexItem />

          {/* Main content area for patient details */}
          <Box flex={1} padding="20px">
            {selectedPatient ? (
              <>
                {patientDetails ? (
                  <>
                    <PatientInfo patientDetails={patientDetails['General Information']} />
                    <TreatmentSummary
                      summaryDetails={patientDetails}
                      patient_text={patientDetails['Relevant_patient_text']}
                      editMode={editMode}
                      onEditChange={handleEditChange}
                    />
                    <FollowUpCarePlan
                      followUpCarePlan={patientDetails}
                      editMode={editMode}
                      onEditChange={handleEditChange}
                    />
                    {editMode ? (
                      <Button onClick={() => handleSave(editedDetails)}>Save Changes</Button>
                    ) : (
                      <Button onClick={toggleEditMode}>Edit</Button>
                    )}
                  </>
                ) : (
                  <Button onClick={onGeneratePlan}>Generate Treatment Plan</Button>
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
