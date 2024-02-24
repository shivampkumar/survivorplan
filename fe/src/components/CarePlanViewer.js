import React, { useEffect, useState } from 'react';
import { FhirService } from './FhirService';

const CarePlanViewer = ({ patientId }) => {
  const [carePlan, setCarePlan] = useState(null);

  useEffect(() => {
    const fetchCarePlan = async () => {
      const fhirService = new FhirService();
      const result = await fhirService.getCarePlan(patientId);
      setCarePlan(result.entry[0].resource || null);
    };

    fetchCarePlan();
  }, [patientId]);

  // Function to render care plan details in a structured format
  const renderCarePlanDetails = (carePlan) => {
    return (
      <div>
        <h3>{carePlan.title}</h3>
        <p><strong>Status:</strong> {carePlan.status}</p>
        <p><strong>Intent:</strong> {carePlan.intent}</p>
        <p><strong>Period:</strong> {carePlan.period.start} to {carePlan.period.end}</p>
        <p><strong>Categories:</strong> {carePlan.category.map(cat => cat.text).join(', ')}</p>
        <p><strong>Contributors:</strong> {carePlan.contributor.map(con => con.name).join(', ')}</p>
        {/* Add more sections as needed */}
      </div>
    );
  };

  return (
    <div>
      {carePlan ? (
        <div>
          <h2>Care Plan for {carePlan.subject.display}</h2>
          {renderCarePlanDetails(carePlan)}
          {/* Extend this section to include treatments, follow-up care, etc., based on your care plan structure */}
        </div>
      ) : (
        <p>No Care Plan found for this patient.</p>
      )}
    </div>
  );
};

export default CarePlanViewer;
