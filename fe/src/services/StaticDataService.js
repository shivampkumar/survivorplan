// Create a new service to handle static data
export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i); // Returns [0, 1, 2, ..., 39]
  }

  static async getPatientData(patientId) {
    // Map the data structure to match what the components expect
    return {
      General_Information: {
        patientId: patientId,
        "Patient Name": `Patient ${patientId}`,
        "Date of Birth": "1960-01-01",
        "Contact Number": "(555) 123-4567",
        "Email": `patient${patientId}@email.com`,
        "Cancer Type": "Breast Cancer",
        "Stage": "Stage II",
        "Diagnosis Date": "2022-01-15"
      },
      Treatment_Summary: {
        "Diagnosis": {
          "Cancer Type": "Breast Cancer",
          "Diagnosis Date": "2022-01-15",
          "Stage": "Stage II"
        },
        "Treatment Details": {
          "Surgery": "Lumpectomy performed on 2022-02-01",
          "Chemotherapy": "4 cycles of AC-T completed on 2022-06-15",
          "Radiation": "30 sessions completed on 2022-08-30"
        },
        "Side Effects": {
          "Current": ["Fatigue", "Mild lymphedema"],
          "Potential Long-term": ["Heart problems", "Secondary cancers"]
        }
      },
      Follow_Up_Care_Plan: {
        "Medical Follow-up": {
          "recommendation": {
            "Schedule": [
              "Oncologist visits every 3 months for first 2 years",
              "Mammogram every 6 months",
              "Annual physical examination"
            ],
            "Tests": [
              "Regular blood work",
              "Bone density scan annually"
            ]
          }
        },
        "Lifestyle Recommendations": {
          "recommendation": {
            "Exercise": [
              "30 minutes moderate activity daily",
              "Include strength training twice weekly"
            ],
            "Diet": [
              "Maintain healthy weight",
              "Eat balanced diet rich in vegetables and fruits"
            ]
          }
        },
        "Psychosocial Support": {
          "recommendation": {
            "Mental Health": [
              "Regular check-ins with mental health professional",
              "Join cancer survivor support group"
            ],
            "Social Support": [
              "Family counseling available",
              "Connect with survivor network"
            ]
          }
        }
      }
    };
  }
} 