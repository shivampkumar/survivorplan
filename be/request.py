from fhirclient import client
import requests
settings = {
    'app_id': 'my_web_app',
    'api_base': 'https://launch.smarthealthit.org/v/r4/sim/WzQsIiIsIiIsIiIsMCwwLDAsIiIsIiIsIiIsIiIsIiIsIiIsIiIsMCwxXQ/fhir'
}
smart = client.FHIRClient(settings=settings)
print(smart.ready)
# url = 'https://launch.smarthealthit.org/v/r4/sim/WzQsIiIsIiIsIiIsMCwwLDAsIiIsIiIsIiIsIiIsIiIsIiIsIiIsMCwxXQ/fhir/metadata'
# response = requests.get(url)
# metadata = response.json()
# print(metadata)
# smart.prepare()
print(smart.ready)
# print(smart.authorize_url)
import fhirclient.models.patient as p
patient = p.Patient.read('a74651a6-8141-4c7e-91b5-a43ce80e6b92', smart.server)
print(patient.birthDate.isostring)

# add a new patient
new_patient = p.Patient({
    "id": "new_patient",
    "name": [
        {
            "family": "Ebert",
            "given": ["Christy"]
        }
    ],
    "birthDate": "1963-06-12"
    })
print(new_patient.as_json())
# '1963-06-12'
print(smart.human_name(patient.name[0]))

patient = p.Patient.read('new_patient', smart.server)
print(patient.as_json())
# 'Christy Ebert'
