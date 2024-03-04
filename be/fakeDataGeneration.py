from faker import Faker
from pymongo import MongoClient
from urllib.parse import quote_plus

# Setup Faker
fake = Faker()

# MongoDB connection
username = os.environ.get('MONGO_USERNAME')
password = os.environ.get('MONGO_PASSWORD')
cluster_address = 'your_cluster_address.mongodb.net'
uri = f"mongodb+srv://{username}:{password}@survivellm.jkaa8ma.mongodb.net/?retryWrites=true&w=majority&appName=survivellm"
client = MongoClient(uri)
db = client.patient_care_db  # Database name
patients = db.patients  # Collection name

# Generate fake data for patients
for _ in range(10):  # Generating data for 10 patients
    patient_data = {
        "name": fake.name(),
        "dob": fake.date_of_birth().strftime("%Y-%m-%d"),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "general_info": {
            "primary_care_provider": fake.name(),
            "other_providers": [fake.name() for _ in range(3)]  # Example for multiple providers
        },
        "treatment_summary": {
            "diagnosis": fake.sentence(),
            "treatment_completed": fake.sentence(),
            "ongoing_treatment": fake.sentence()
        }
    }
    patients.insert_one(patient_data)

print("Fake patient data inserted into MongoDB.")
