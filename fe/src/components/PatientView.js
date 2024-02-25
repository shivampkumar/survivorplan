import React from 'react';
import PatientInfo from './PatientInfo';
import TreatmentSummary from './TreatmentSummary';

const PatientView = ({ patientDetails }) => {
  // For patients, editMode is always false, making fields non-editable
  const editMode = false;
  if (!patientDetails) {
    return <div>Loading details...</div>;
  }
  return (
    <div>
      <PatientInfo patientDetails={patientDetails['General Information']} />
      {patientDetails['Treatment Summary']
        ? <TreatmentSummary summaryDetails={patientDetails['Treatment Summary']} editMode={editMode} />
        : <div>No treatment plan created yet...</div>
      }
      {patientDetails['Follow Up Care Plan']
        ? <div>Follow up care plan: {patientDetails['Follow Up Care Plan']}</div>
        : null
      }
    </div>
  );
};

export default PatientView;
