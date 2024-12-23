import { SCPs } from '../data/SCPs'; // Make sure to import the SCPs data

export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i); // Keep this as is since we have 40 patients
  }

  static async getPatientData(patientId) {
    const scp = SCPs[patientId]; // Get the specific patient's SCP data
    
    if (!scp) {
      throw new Error(`No SCP data found for patient ${patientId}`);
    }

    // Map the SCP data to match the expected structure
    return {
      General_Information: {
        patientId: patientId,
        "Patient Name": scp.patientName || `Patient ${patientId}`,
        "Date of Birth": scp.dateOfBirth,
        "Contact Number": scp.contactNumber,
        "Email": scp.email,
        "Cancer Type": scp.cancerType,
        "Stage": scp.stage,
        "Diagnosis Date": scp.diagnosisDate
      },
      Treatment_Summary: {
        "Diagnosis": {
          "Cancer Type": scp.cancerType,
          "Diagnosis Date": scp.diagnosisDate,
          "Stage": scp.stage
        },
        "Treatment Details": {
          "Surgery": scp.surgeryDetails,
          "Chemotherapy": scp.chemotherapyDetails,
          "Radiation": scp.radiationDetails
        },
        "Side Effects": {
          "Current": scp.currentSideEffects || [],
          "Potential Long-term": scp.potentialLongTermEffects || []
        }
      },
      Follow_Up_Care_Plan: {
        "Medical Follow-up": {
          "recommendation": {
            "Schedule": scp.followUpSchedule || [],
            "Tests": scp.recommendedTests || []
          }
        },
        "Lifestyle Recommendations": {
          "recommendation": {
            "Exercise": scp.exerciseRecommendations || [],
            "Diet": scp.dietRecommendations || []
          }
        },
        "Psychosocial Support": {
          "recommendation": {
            "Mental Health": scp.mentalHealthRecommendations || [],
            "Social Support": scp.socialSupportRecommendations || []
          }
        }
      }
    };
  }
} 