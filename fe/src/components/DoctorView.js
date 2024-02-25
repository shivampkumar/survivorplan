import React, { useState, useEffect } from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';
import FollowUpCarePlan from './FollowUpCarePlan';
import PatientSidebar from './PatientSidebar'; // Import the sidebar
import axios from 'axios';

import { Button, Box, Divider } from '@mui/material';

const API_BASE_URL = 'http://20.168.8.23:8080/api';

const DoctorView = ({ patients }) => {
  const [editMode, setEditMode] = useState(false);
  const [editedDetails, setEditedDetails] = useState({});
  const [selectedPatient, setSelectedPatient] = useState(null); // Track selected patient
  const [patientDetails, setPatientDetails] = useState(null); // New state for patient details

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
      axios.post(`${API_BASE_URL}/patients/${selectedPatient.id}/generate_plan`)
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

  const handleSave = () => {
    onSaveChanges(editedDetails);
    setEditMode(false);
  };

  const onSelectPatient = (patient) => {
    setSelectedPatient(patient);
  };

  // Example layout with sidebar and main content
  return (
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
                <TreatmentSummary summaryDetails={patientDetails['Treatment Summary']} editMode={editMode} onEditChange={handleEditChange} />
                <FollowUpCarePlan
                  followUpCarePlan={patientDetails['Follow Up Care Plan']}
                  editMode={editMode}
                  onEditChange={handleEditChange}
                />
                {editMode ? (
                  <Button onClick={handleSave}>Save Changes</Button>
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
  );
};

export default DoctorView;
