export class StaticDataService {
  static getPatientIds() {
    return Array.from({ length: 40 }, (_, i) => i);
  }

  static async getAllPatients() {
    try {
      const patientIds = this.getPatientIds();
      const patients = await Promise.all(
        patientIds.map(async (id) => {
          const treatmentSummary = await import(`./SCPs/${id}/${id}_treatment_summary.json`);
          const patientInfo = this.generatePatientInfo(id);
          return {
            patientId: id,
            "Patient Name": patientInfo.patientName,
            "Cancer Type": treatmentSummary.Diagnosis?.[0]?.["Cancer Type"] || "Unknown"
          };
        })
      );
      return patients;
    } catch (error) {
      console.error('Error loading patients:', error);
      return [];
    }
  }

  static generatePatientInfo(patientId) {
    return {
      patientName: `Patient_${patientId}`,
      dateOfBirth: `1960-01-${String(patientId + 1).padStart(2, '0')}`,
      gender: patientId % 2 === 0 ? 'Male' : 'Female',
      contactNumber: `555-000-${String(patientId).padStart(4, '0')}`,
      email: `patient${patientId}@example.com`
    };
  }

  static async getPatientData(patientId) {
    try {
      // Load all required JSON files for the patient
      const treatmentSummary = await import(`./SCPs/${patientId}/${patientId}_treatment_summary.json`);
      const surveillanceTests = await import(`./SCPs/${patientId}/${patientId}_Cancer surveillance and other recommended tests for cancer monitoring.json`);
      const lifestyleRecs = await import(`./SCPs/${patientId}/${patientId}_Lifestyle and behavior recommendations for cancer survivors.json`);
      const symptoms = await import(`./SCPs/${patientId}/${patientId}_Already experienced symptoms or side effects.json`);
      const longTermEffects = await import(`./SCPs/${patientId}/${patientId}_Possible late and long-term effects of cancer treatment.json`);
      const otherIssues = await import(`./SCPs/${patientId}/${patientId}_Possible other issues that cancer survivors may experience.json`);
      const references = await import(`./SCPs/${patientId}/${patientId}_References to helpful resources for cancer survivors.json`);

      // Load reference context files
      const surveillanceContext = await import(`./SCPs/${patientId}/${patientId}_retrieved_context_Cancer surveillance and other recommended tests for cancer monitoring.json`);
      const lifestyleContext = await import(`./SCPs/${patientId}/${patientId}_retrieved_context_Lifestyle and behavior recommendations for cancer survivors.json`);
      const longTermEffectsContext = await import(`./SCPs/${patientId}/${patientId}_retrieved_context_Possible late and long-term effects of cancer treatment.json`);
      const referencesContext = await import(`./SCPs/${patientId}/${patientId}_retrieved_context_References to helpful resources for cancer survivors.json`);

      const patientInfo = this.generatePatientInfo(patientId);

      return {
        General_Information: {
          patientId: patientId,
          "Patient Name": patientInfo.patientName,
          "Date of Birth": patientInfo.dateOfBirth,
          "Contact Number": patientInfo.contactNumber,
          "Email": patientInfo.email,
          "Cancer Type": treatmentSummary.Diagnosis?.[0]?.["Cancer Type"] || "",
          "Stage": treatmentSummary.Diagnosis?.[0]?.["Cancer Stage"] || "",
          "Diagnosis Date": treatmentSummary.Diagnosis?.[0]?.["Diagnosis Date"] || ""
        },
        Treatment_Summary: treatmentSummary,
        Follow_Up_Care_Plan: {
          "Medical Follow-up": {
            "recommendation": {
              "Schedule": [], // This could be populated from another file if available
              "Tests": surveillanceTests["Cancer surveillance and other recommended tests for cancer monitoring"]?.map(test => ({
                ...test,
                references: surveillanceContext.retrieved_context[test["Retrieved context id"]]?.text || ""
              })) || []
            }
          },
          "Lifestyle Recommendations": {
            "recommendation": {
              "Exercise": lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"]
                ?.filter(rec => rec.Lifestyle.toLowerCase().includes("physical activity") || rec.Lifestyle.toLowerCase().includes("exercise"))
                .map(rec => ({
                  ...rec,
                  references: lifestyleContext.retrieved_context[rec["Retrieved context id"]]?.text || ""
                })) || [],
              "Diet": lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"]
                ?.filter(rec => rec.Lifestyle.toLowerCase().includes("diet") || rec.Lifestyle.toLowerCase().includes("nutrition"))
                .map(rec => ({
                  ...rec,
                  references: lifestyleContext.retrieved_context[rec["Retrieved context id"]]?.text || ""
                })) || []
            }
          },
          "Psychosocial Support": {
            "recommendation": {
              "Mental Health": lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"]
                ?.filter(rec => rec.Lifestyle.toLowerCase().includes("mental") || rec.Lifestyle.toLowerCase().includes("psycho"))
                .map(rec => ({
                  ...rec,
                  references: lifestyleContext.retrieved_context[rec["Retrieved context id"]]?.text || ""
                })) || [],
              "Social Support": lifestyleRecs["Lifestyle and behavior recommendations for cancer survivors"]
                ?.filter(rec => rec.Lifestyle.toLowerCase().includes("social") || rec.Lifestyle.toLowerCase().includes("support"))
                .map(rec => ({
                  ...rec,
                  references: lifestyleContext.retrieved_context[rec["Retrieved context id"]]?.text || ""
                })) || []
            }
          },
          "Late and Long-term Effects": {
            "recommendation": {
              "Effects": longTermEffects["Possible late and long-term effects of cancer treatment"]?.map(effect => ({
                ...effect,
                references: longTermEffectsContext.retrieved_context[effect["Retrieved context id"]]?.text || ""
              })) || []
            }
          },
          "Other Issues": {
            "recommendation": {
              "Issues": otherIssues["Possible other issues that cancer survivors may experience"]?.map(issue => ({
                ...issue,
                references: longTermEffectsContext.retrieved_context[issue["Retrieved context id"]]?.text || ""
              })) || []
            }
          },
          "Helpful Resources": {
            "recommendation": {
              "Resources": references["References to helpful resources for cancer survivors"]?.map(resource => ({
                ...resource,
                references: referencesContext.retrieved_context[resource["Retrieved context id"]]?.text || ""
              })) || []
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