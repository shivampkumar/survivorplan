import { SCPs } from '../data/SCPs';

interface SystemicTherapyAgent {
  name: string;
  endDate: string;
}

interface TestRecommendation {
  "Test type": string;
  "When / how often": string;
  "Frequency (in weeks)": number;
  "Explanation": string;
  "Retrieved context id": number;
}

interface LifestyleRecommendation {
  "Lifestyle": string;
  "Explanation": string;
  "Retrieved context id": number;
}

export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i);
  }

  static async getPatientData(patientId: number) {
    try {
      // Load the required JSON files for the patient
      const treatmentSummary = await import(`./SCPs/${patientId}/${patientId}_treatment_summary.json`);
      const surveillanceTests = await import(`./SCPs/${patientId}/${patientId}_Cancer surveillance and other recommended tests for cancer monitoring.json`);
      const lifestyleRecs = await import(`./SCPs/${patientId}/${patientId}_Lifestyle and behavior recommendations for cancer survivors.json`);
      const symptoms = await import(`./SCPs/${patientId}/${patientId}_Already experienced symptoms or side effects.json`);

      return {
        treatmentSummary: {
          Diagnosis: {
            "Cancer type": treatmentSummary.Diagnosis?.[0]?.["Cancer Type"] || "",
            "Diagnosis Date": treatmentSummary.Diagnosis?.[0]?.["Diagnosis Date"] || "",
            "Cancer Stage": treatmentSummary.Diagnosis?.[0]?.["Cancer Stage"] || "",
            "Molecular Markers": treatmentSummary.Diagnosis?.[0]?.["Molecular Markers"] || ""
          },
          Surgery: {
            conducted: treatmentSummary["Surgery Conducted (Yes/No)"]?.[0]?.["Surgery Conducted (Yes/No)"] || "No",
            procedure: treatmentSummary.Surgery_Information?.[0]?.["Surgery Procedure"] || "",
            dates: treatmentSummary.Surgery_Information?.[0]?.["Surgery Date(s) (year)"] || "",
            location: treatmentSummary.Surgery_Information?.[0]?.["Surgery Location"] || "",
            findings: treatmentSummary.Surgery_Information?.[0]?.["Surgery Findings"] || ""
          },
          RadiationTreatment: {
            conducted: treatmentSummary["Radiation Treatment Conducted (Yes/No)"]?.[0]?.["Radiation Treatment Conducted (Yes/No)"] || "No",
            procedure: treatmentSummary.Radiation_Treatment_Information?.[0]?.["Radiation Treatment Procedure"] || "",
            dates: treatmentSummary.Radiation_Treatment_Information?.[0]?.["Radiation Treatment Date(s) (year)"] || "",
            location: treatmentSummary.Radiation_Treatment_Information?.[0]?.["Radiation Treatment Location"] || ""
          },
          SystemicTherapy: {
            conducted: treatmentSummary["Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)"]?.[0]?.["Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)"] || "No",
            agents: treatmentSummary["Agents Used in Completed Treatments"] || []
          },
          PersistentSymptoms: {
            present: symptoms?.present || "No",
            symptoms: symptoms?.symptoms || []
          }
        },
        followUpCarePlan: {
          "Cancer Surveillance or Other Recommended Tests": {
            recommendation: {
              "Cancer Surveillance or Other Recommended Tests": 
                surveillanceTests["Cancer surveillance and other recommended tests for cancer monitoring"] || []
            }
          },
          "Lifestyle and behavior": {
            recommendation: {
              "Lifestyle and behavior": 
                lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"] || []
            }
          }
        }
      };
    } catch (error) {
      console.error(`Error loading data for patient ${patientId}:`, error);
      throw new Error(`Failed to load data for patient ${patientId}`);
    }
  }
} 