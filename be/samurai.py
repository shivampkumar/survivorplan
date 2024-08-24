from dotenv import load_dotenv
from os.path import join, dirname
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


import aidbox;

from aidbox.resource.patient import Patient
from aidbox.resource.condition import Condition
from aidbox.resource.procedure import Procedure
from aidbox.resource.medicationstatement import MedicationStatement
from aidbox.resource.observation import Observation
from aidbox.resource.practitioner import Practitioner
from aidbox.base import Reference
from aidbox.base import Page, Count, Sort, Where


def get_patient_by_id(patient_id):
    return Patient.from_id(patient_id)

def fetch_related_resources(patient_id):
    related_resources = {}
    #import ipdb; ipdb.set_trace()
    # Fetch conditions
    conditions = Condition.get(Where('subject', f"Patient/{patient_id}"))
    related_resources['conditions'] = [condition.model_dump_json(exclude_unset=True) for condition in conditions]

    # Fetch procedures
    procedures = Procedure.get(Where('subject', f"Patient/{patient_id}"))
    related_resources['procedures'] = [procedure.model_dump_json(exclude_unset=True) for procedure in procedures]

    # Fetch medication statements
    medication_statements = MedicationStatement.get(Where('subject', f"Patient/{patient_id}"))
    related_resources['medication_statements'] = [medication_statement.model_dump_json(exclude_unset=True) for medication_statement in medication_statements]

    # Fetch observations
    observations = Observation.get(Where('subject', f"Patient/{patient_id}"))
    related_resources['observations'] = [observation.model_dump_json(exclude_unset=True) for observation in observations]

    return related_resources

def fetch_practitioners():
    practitioners = Practitioner.get()
    return [practitioner.model_dump_json(exclude_unset=True) for practitioner in practitioners]


def get_patient_data(patient_id):
    #import ipdb; ipdb.set_trace()
    patient = get_patient_by_id(patient_id)
    related_resources = fetch_related_resources(patient_id)
    practitioners = fetch_practitioners()

    combined_data = {
        'patient': patient.model_dump_json(exclude_unset=True),
        'related_resources': related_resources,
        'practitioners': practitioners
    }
    print(combined_data)
    return combined_data

patient = get_patient_by_id("p13491")
patient.name[0].given[0] = "Sarah"
patient.name[0].family = "Williams"
patient.save()

# print(get_patient_data("p6269"))

# patient_id = "p6269"  # Replace with actual patient ID
# re = Reference(reference=f"Patient/{patient_id}")
# print("RE", re)

# # Ensure you print all conditions to verify they exist
# print("All conditions:", Condition.get())

# # Using the correct Where clause to filter by subject reference
# condition = Condition.get(Where('subject',re))
# # condition = Condition.get(Where('subject', Reference(reference=f"Patient/{patient_id}")))
# print("Filtered conditions:", condition)
# condition2 = Condition.get(Where('subject', f"Patient/{patient_id}"))
# print("Filtered conditions2:", condition2)
# patient_data = get_patient_data(patient_id)