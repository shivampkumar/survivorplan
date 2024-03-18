import React from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';
import FollowUpCarePlan from './FollowUpCarePlan';

const PatientView = ({ patientDetails }) => {
  // For patients, editMode is always false, making fields non-editable
  const editMode = false;
  if (!patientDetails) {
    return <div>Loading details...</div>;
  }
  console.log("pateint details", patientDetails);
  return (
    <div>
      <PatientInfo patientDetails={patientDetails['General Information']} />
      {patientDetails['Treatment Summary']
        ? <TreatmentSummary summaryDetails={patientDetails} patient_text={patientDetails['Relevant_patient_text']} editMode={editMode}/>
        : <div>No treatment plan created yet...</div>
      }
      {patientDetails['Follow Up Care Plan']
        ? <FollowUpCarePlan
          followUpCarePlan={patientDetails}
          editMode={editMode}
        />
        : null
      }
    </div>
  );
};

export default PatientView;
