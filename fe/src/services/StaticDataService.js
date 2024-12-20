// Create a new service to handle static data
export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i); // Returns [0, 1, 2, ..., 39]
  }

  static async getPatientData(patientId) {
    // This would actually load the JSON files from SCPs folder
    // For now simulating the structure based on SCPs/0/ folder
    return {
      General_Information: {
        // Dummy data since not provided in SCPs
        patientId: patientId,
        name: `Patient ${patientId}`,
        dateOfBirth: "1960-01-01",
        contactNumber: "(555) 123-4567",
        email: `patient${patientId}@email.com`
      },
      Treatment_Summary: {
        // Structure from 0_treatment_summary.json
        Diagnosis: {
          "Cancer type": "adenocarcinoma of the pancreas",
          "Diagnosis Date": "October 24",
          "Cancer Stage": "locally advanced",
          "Molecular Markers": ""
        },
        Surgery: {
          conducted: "No",
          procedure: "",
          dates: "",
          location: "",
          findings: ""
        },
        // ... other treatment summary fields
      },
      Follow_Up_Care_Plan: {
        "Already experienced symptoms or side effects": [
          // From 0_Already experienced symptoms or side effects.json
          {
            "Symptom": "Peripheral neuropathy",
            "Explanation": "Patient reports numbness and tingling...",
            "Retrieved context id": 5
          }
        ],
        "Cancer surveillance and other recommended tests": [
          // From 0_Cancer surveillance and other recommended tests for cancer monitoring.json
          {
            "Test type": "Imaging (CT scan)",
            "When / how often": "Every 3 months",
            "Explanation": "Regular imaging is recommended...",
            "Retrieved context id": 20
          }
        ],
        "Lifestyle and behavior recommendations": [
          // From 0_Lifestyle and behavior recommendations for cancer survivors.json
          {
            "Lifestyle": "Regular physical activity",
            "Explanation": "Engage in moderate exercise...",
            "Retrieved context id": 2
          }
        ],
        "Possible late and long-term effects": [
          // From 0_Possible late and long-term effects of cancer treatment.json
          {
            "Treatment effect": "Peripheral neuropathy",
            "Explanation": "Numbness and tingling...",
            "Retrieved context id": 9
          }
        ],
        "Possible other issues": [
          // From 0_Possible other issues that cancer survivors may experience.json
          {
            "Issue": "Depression and anxiety",
            "Explanation": "The patient is dealing with...",
            "Retrieved context id": 6
          }
        ],
        "References to helpful resources": [
          // From 0_References to helpful resources for cancer survivors.json
          {
            "Resource": "ACS Survivorship Center Web site",
            "Explanation": "This resource provides comprehensive...",
            "Retrieved context id": 1
          }
        ],
        retrieved_context: {
          // Combined context from all _retrieved_context_ files
          // Will be used for references
        }
      }
    };
  }
} 