// Create a new service to handle static data
export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i); // Returns [0, 1, 2, ..., 39]
  }

  static async getPatientData(patientId: number) {
    // In a real implementation, this would load JSON files from SCPs folder
    // For now, we'll simulate the structure based on the files in SCPs/0/
    return {
      treatmentSummary: {
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
        RadiationTreatment: {
          conducted: "No",
          procedure: "",
          dates: "",
          location: ""
        },
        SystemicTherapy: {
          conducted: "Yes",
          agents: [
            { name: "gemcitabine", endDate: "" },
            { name: "Abraxane", endDate: "" }
          ]
        },
        PersistentSymptoms: {
          present: "Yes",
          symptoms: ["numbness and tingling in hands"]
        }
      },
      followUpCarePlan: {
        "Cancer Surveillance or Other Recommended Tests": {
          recommendation: {
            "Cancer Surveillance or Other Recommended Tests": [
              {
                "Test type": "Imaging (CT scan)",
                "When / how often": "Every 3 months in Year 1, every 6 months in Year 2, and annually in Years 3-5",
                "Frequency (in weeks)": 12,
                "Explanation": "Regular imaging is recommended...",
                "Retrieved context id": 20
              }
              // ... other tests
            ]
          }
        },
        "Lifestyle and behavior": {
          recommendation: {
            "Lifestyle and behavior": [
              {
                "Lifestyle": "Engage in regular physical activity",
                "Explanation": "Regular physical activity can help maintain...",
                "Retrieved context id": 2
              }
              // ... other recommendations
            ]
          }
        }
        // ... other sections
      }
    };
  }
} 