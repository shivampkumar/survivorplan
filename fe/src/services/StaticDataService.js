export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i);
  }

  static async getPatientData(patientId) {
    try {
      // Load the required JSON files for the patient
      const treatmentSummary = await import(`./SCPs/${patientId}/${patientId}_treatment_summary.json`);
      const surveillanceTests = await import(`./SCPs/${patientId}/${patientId}_Cancer surveillance and other recommended tests for cancer monitoring.json`);
      const lifestyleRecs = await import(`./SCPs/${patientId}/${patientId}_Lifestyle and behavior recommendations for cancer survivors.json`);
      const symptoms = await import(`./SCPs/${patientId}/${patientId}_Already experienced symptoms or side effects.json`);

      return {
        General_Information: {
          patientId: patientId,
          "Patient Name": `Patient ${patientId}`,
          "Date of Birth": treatmentSummary.Diagnosis?.[0]?.["Date of Birth"] || "",
          "Contact Number": treatmentSummary.Diagnosis?.[0]?.["Contact Number"] || "",
          "Email": treatmentSummary.Diagnosis?.[0]?.["Email"] || "",
          "Cancer Type": treatmentSummary.Diagnosis?.[0]?.["Cancer Type"] || "",
          "Stage": treatmentSummary.Diagnosis?.[0]?.["Cancer Stage"] || "",
          "Diagnosis Date": treatmentSummary.Diagnosis?.[0]?.["Diagnosis Date"] || ""
        },
        Treatment_Summary: {
          "Diagnosis": {
            "Cancer Type": treatmentSummary.Diagnosis?.[0]?.["Cancer Type"] || "",
            "Diagnosis Date": treatmentSummary.Diagnosis?.[0]?.["Diagnosis Date"] || "",
            "Stage": treatmentSummary.Diagnosis?.[0]?.["Cancer Stage"] || ""
          },
          "Treatment Details": {
            "Surgery": treatmentSummary["Surgery Conducted (Yes/No)"]?.[0]?.["Surgery Conducted (Yes/No)"] === "Yes"
              ? treatmentSummary.Surgery_Information?.[0]?.["Surgery Procedure"] || ""
              : "No surgery conducted",
            "Chemotherapy": treatmentSummary["Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)"]?.[0]?.["Systemic Therapy Conducted (Chemotherapy, hormonal therapy, other)"] === "Yes"
              ? (treatmentSummary["Agents Used in Completed Treatments"] || []).map(agent => agent.name).join(", ")
              : "No chemotherapy conducted",
            "Radiation": treatmentSummary["Radiation Treatment Conducted (Yes/No)"]?.[0]?.["Radiation Treatment Conducted (Yes/No)"] === "Yes"
              ? treatmentSummary.Radiation_Treatment_Information?.[0]?.["Radiation Treatment Procedure"] || ""
              : "No radiation conducted"
          },
          "Side Effects": {
            "Current": symptoms?.symptoms || [],
            "Potential Long-term": [] // This could be populated from another file if available
          }
        },
        Follow_Up_Care_Plan: {
          "Medical Follow-up": {
            "recommendation": {
              "Schedule": [], // This could be populated from another file if available
              "Tests": surveillanceTests["Cancer surveillance and other recommended tests for cancer monitoring"] || []
            }
          },
          "Lifestyle Recommendations": {
            "recommendation": {
              "Exercise": (lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"] || [])
                .filter(rec => rec.Lifestyle.toLowerCase().includes("physical activity") || rec.Lifestyle.toLowerCase().includes("exercise")),
              "Diet": (lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"] || [])
                .filter(rec => rec.Lifestyle.toLowerCase().includes("diet") || rec.Lifestyle.toLowerCase().includes("nutrition"))
            }
          },
          "Psychosocial Support": {
            "recommendation": {
              "Mental Health": (lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"] || [])
                .filter(rec => rec.Lifestyle.toLowerCase().includes("mental") || rec.Lifestyle.toLowerCase().includes("psycho")),
              "Social Support": (lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"] || [])
                .filter(rec => rec.Lifestyle.toLowerCase().includes("social") || rec.Lifestyle.toLowerCase().includes("support"))
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