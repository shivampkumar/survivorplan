import React, { useState } from 'react';
import { FhirService } from './FhirService';

const PatientSelector = () => {
  const [query, setQuery] = useState('');
  const [patients, setPatients] = useState([]);

  const handleSearch = async () => {
    const fhirService = new FhirService();
    const result = await fhirService.searchPatient(query);
    setPatients(result.entry || []);
  };

  return (
    <div>
      <input 
        type="text" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Search Patients" 
      />
      <button onClick={handleSearch}>Search</button>
      <ul>
        {patients.map((patient) => (
          <li key={patient.resource.id}>{patient.resource.name[0].text}</li>
        ))}
      </ul>
    </div>
  );
};

export default PatientSelector;