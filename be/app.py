from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson import ObjectId
from urllib.parse import quote_plus
import os
from celery import Celery
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from flask import send_file
from celery_app import make_celery
from dotenv import load_dotenv
load_dotenv()
import json
import time
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.service_context import ServiceContext
from init.init_api import init_api
from care_plan_gen.care_plan_gen import extract_json_text_from_response,get_care_recommendation_2stage_patient_query,get_relevant_patient_text,load_knowledge_base
from care_plan_gen.rectifier import rectifier
from care_plan_gen.prompts import get_care_prompts,get_treatment_summarizer_prompts,get_general_info_prompt
from utils.rag_utils import  create_query_engine,dict_to_text_file
from utils.rag_utils import treatment_summary_query_engine
from care_plan_gen.pdf_gen import SurvGPT_PDF_2stage
from aidbox.resource.patient import Patient
from aidbox.resource.condition import Condition
from aidbox.resource.procedure import Procedure
from aidbox.resource.medicationstatement import MedicationStatement
from aidbox.resource.observation import Observation
from aidbox.resource.practitioner import Practitioner
from aidbox.base import Reference
from aidbox.base import Page, Count, Sort, Where

app = Flask(__name__)
print("Name",__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = make_celery(app)
bcrypt = Bcrypt(app)

username = os.environ.get('MONGO_USERNAME')
password = os.environ.get('MONGO_PASSWORD')
username = quote_plus(username)
password = quote_plus(password)

# MongoDB setup
uri = f"mongodb+srv://{username}:{password}@survivellm.jkaa8ma.mongodb.net/?retryWrites=true&w=majority&appName=survivellm"
client = MongoClient(uri)

db = client.patient_care_db
users = db.users
patient_records = db['patient_records']

def patient_encoder(patient):
    if isinstance(patient, ObjectId):
        return str(patient)
    raise TypeError(f"Object of type {patient.__class__.__name__} is not JSON serializable")

@app.route('/api/hello', methods=['GET'])
@cross_origin()
def get_users():
    # Create a dummy result just to test if the API is working
    
    return jsonify({'message': 'API is working'}), 200

@app.route('/api/register', methods=['POST','OPTIONS'])
@cross_origin()
def register():
    user_data = request.json
    user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
    
    # Check if user already exists
    if users.find_one({'email': user_data['email']}):
        return jsonify({'message': 'User already exists'}), 400
    
    users.insert_one(user_data)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/patients', methods=['GET'])
@cross_origin()
def get_patients():
    patients = patient_records.find({}, {"patientID": 1, "General Information.Patient Name": 1})

    # Convert each patient document to a dict and ObjectId to str
    patients_list = []
    for patient in patients:
        patient['_id'] = patient_encoder(patient['_id'])  # Convert ObjectId to str
        patients_list.append(patient)

    return jsonify(patients_list)

@app.route('/api/patientsFH', methods=['GET'])
@cross_origin()
def get_patientsFH():
    patients = Patient.get()
    patients_list = []
    for patient in patients:
        pat = {}
        pat['_id'] =  patient.id
        pat['patientID'] = patient.id
        if patient.name:
            for name in patient.name:
                if name.given and name.family:
                    given_names = ' '.join(name.given)
                    full_name = f"{given_names} {name.family}"
                    pat['General Information.Patient Name'] = full_name
                    pat['name'] = full_name
                    pat['Patient Name'] = full_name
                else:
                    pat['General Information.Patient Name'] = "Unknown"
                    pat['name'] = "Unknown"
                    pat['Patient Name'] = "Unknown"
        else:
            pat['General Information.Patient Name'] = "Unknown"
            pat['name'] = "Unknown"
            pat['Patient Name'] = "Unknown"
        
        patients_list.append(pat)
    print(patients_list)
    return jsonify(patients_list)

# @app.route('/api/patients/<patientID>', methods=['GET'])
# @cross_origin()
# def get_patient_details(patientID):
#     patient_details = patient_records.find_one({"patientID": patientID}, {"_id": 0})
#     if patient_details:
#         return jsonify(patient_details)
#     else:
#         return jsonify({"error": "Patient not found"}), 404


@app.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    user_data = request.json
    user = users.find_one({'email': user_data['email']})

    if user and bcrypt.check_password_hash(user['password'], user_data['password']):
        return jsonify({'message': 'Login successful', 'role': user['role'], 'patientID' : 'p20952'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@celery.task(name="app.generate_patient_data_task")
def generate_patient_data_task(patient_id):
    patient_data = get_patient_data(patient_id)
    general_dict, treatment_sum_dict, follow_up_care_plan, follow_up_care_plan_rect, removed_care_recommendations, time_dict = create_care_plan(str(patient_data))

    patient_data_json = {
        "patientID": patient_id,
        "General Information": general_dict['General Information'],
        "Treatment Summary": treatment_sum_dict['Treatment Summary'],
        "Follow Up Care Plan": follow_up_care_plan_rect,
    }

    patient_records.update_one(
        {"patientID": patient_id},
        {"$set": patient_data_json, "$unset": {"task_id": ""}}
    )
    return {'message': 'Patient data inserted successfully'}

@app.route('/api/patients/<patientID>', methods=['GET'])
@cross_origin()
def get_patient_details(patientID):
    patient_details = patient_records.find_one({"patientID": patientID}, {"_id": 0})
    print("Received patient details", patient_details)
    if patient_details:
        if "task_id" in patient_details:
            task = generate_patient_data_task.AsyncResult(patient_details["task_id"])
            if task.state in ["PENDING", "STARTED", "RETRY"]:
                return jsonify({'task_id': task.id, 'status': task.state}), 202
            elif task.state == "SUCCESS":
                return jsonify(patient_details)
            else:
                # Task failed, remove task_id and proceed to create a new task
                patient_records.update_one({"patientID": patientID}, {"$unset": {"task_id": ""}})
                task = generate_patient_data_task.delay(patientID)
                patient_records.update_one({"patientID": patientID}, {"$set": {"task_id": task.id}})
                return jsonify({'task_id': task.id}), 202
        else:
            return jsonify(patient_details)
    else:
        # Patient details not found, create a new task
        task = generate_patient_data_task.delay(patientID)
        patient_records.insert_one({"patientID": patientID, "task_id": task.id})
        return jsonify({'task_id': task.id}), 202

@app.route('/api/generate_pdf/<patientID>', methods=['GET'])
@cross_origin()
def generate_pdf(patientID):
    patient_details = patient_records.find_one({"patientID": patientID})
    
    if not patient_details:
        return jsonify({'message': 'Patient not found'}), 404
    
    # Create a PDF in memory
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"Care Plan for Patient: {patient_details['General Information']['Patient Name']}")

    # Start adding details
    y_position = height - 80
    line_height = 14
    c.setFont("Helvetica", 12)

    def draw_text(text, y_position):
        if y_position < 40:  # If near the bottom of the page, create a new page
            c.showPage()
            y_position = height - 40
        c.drawString(100, y_position, text)
        return y_position - line_height

    # General Information
    y_position = draw_text("General Information:", y_position)
    for key, value in patient_details['General Information'].items():
        y_position = draw_text(f"{key}: {value}", y_position)

    # Treatment Summary
    y_position -= line_height  # Add a small gap
    y_position = draw_text("Treatment Summary:", y_position)
    for section, details in patient_details['Treatment Summary'].items():
        y_position = draw_text(f"{section}:", y_position)
        if isinstance(details, dict):
            for key, value in details.items():
                y_position = draw_text(f"  {key}: {value}", y_position)
        else:
            y_position = draw_text(f"  {details}", y_position)

    # Follow-Up Care Plan
    y_position -= line_height  # Add a small gap
    y_position = draw_text("Follow-Up Care Plan:", y_position)
    for section, recommendations in patient_details['Follow Up Care Plan'].items():
        y_position = draw_text(f"{section}:", y_position)
        if 'recommendation' in recommendations and isinstance(recommendations['recommendation'], dict):
            for key, value in recommendations['recommendation'].items():
                if isinstance(value, list):
                    for item in value:
                        y_position = draw_text(f"  {item}", y_position)
                else:
                    y_position = draw_text(f"  {key}: {value}", y_position)

    c.save()

    # Rewind the buffer to the beginning so Flask can read it correctly
    pdf_buffer.seek(0)
    
    return send_file(pdf_buffer, as_attachment=True, download_name=f"CarePlan_{patientID}.pdf", mimetype='application/pdf')

@app.route('/api/status/<task_id>', methods=['GET'])
@cross_origin()
def task_status(task_id):
    task = generate_patient_data_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

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
    patient = Patient.from_id(patient_id)
    related_resources = fetch_related_resources(patient_id)
    practitioners = fetch_practitioners()

    combined_data = {
        'patient': patient.model_dump_json(exclude_unset=True),
        'related_resources': related_resources,
        'practitioners': practitioners
    }
    print(combined_data)
    return combined_data



def create_care_plan(patient_data,llm_type = "gpt-35-turbo-16k",embedding_type = 'text-embedding-3-large'):
    '''
    Takes in patient data and generates the care plan
    Args:
    patient_data: Currently in text format
    llm_type: The type of language model to use
                GPT-3.5: "gpt-35-turbo-16k"
                GPT-4: "gpt-4"
    embedding_type: The type of embedding to use
                    Ada: "text-embedding-ada-002"
                    BGE large: "BAAI/bge-large-en-v1.5"
    
    Returns:
     general_dict: A dictionary containing the general information of the patient
     treatment_sum_dict: A dictionary containing the treatment summary of the patient
     follow_up_care_plan: A dictionary containing the follow up care plan of the patient
     follow_up_care_plan_rect: A dictionary containing the rectified follow up care plan of the patient
     removed_care_recommendations: A dictionary containing the removed care recommendations of the patient
     time_dict: A dictionary containing the time information of the patient
    '''
    ############################################
    # Azure API parameters
    #import ipdb; ipdb.set_trace()
    api_key = os.getenv('AZURE_API_KEY')
    azure_endpoint = os.getenv('AZURE_ENDPOINT')
    api_version = os.getenv('AZURE_API_VERSION')
    model = llm_type
    deployment_name= llm_type
    temperature=0
    # for LLM small
    model_35 = 'gpt-35-turbo-16k'  
    deployment_name_35 = 'gpt-35-turbo-16k'
    temperature_35 = 0
    # embedding model
    embedding_model = embedding_type
    #rectification parameters   
    rect_temp = 0
    rect_iter = 1#3
    ############################################
    # Other Parameters
    knowledge_path = './knowledge_base/knowledge_bases'
    # Output json
    time_dict = {}
    general_dict = {}
    treatment_sum_dict = {'Treatment Summary':{},
                            'Relevant_patient_text':{}}
    follow_up_care_plan = {}
    follow_up_care_plan_rect = {}
    removed_care_recommendations = {}
    ############################################
    
    ## Init API, LLM and Embedding Models
    init_api(api_key, azure_endpoint, api_version)
    
    print(f'Initializing smaller LLM: {model_35}, temperature: {temperature_35}')
    llm_small = AzureOpenAI(
            model=model_35,
            deployment_name=deployment_name_35,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            temperature=temperature_35,
            )

    # Initialize the LLM
    print(f'Initializing LLM: {model}, temperature: {temperature}')
    llm = AzureOpenAI(
            model=model,
            deployment_name=deployment_name,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            temperature=temperature,
            )

    # #Initialize rectifier
    print(f'Initializing LLM for rectification: {model}, temperature: {rect_temp}')
    llm_rect = AzureOpenAI(
            model=model,
            deployment_name=deployment_name,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            temperature=rect_temp,
            )

    # Initialize the text embedder

    # To use text ada embedding
    print(f'Initializing Embedding Model: {embedding_model}')
    text_embedder = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="text-embedding-ada-002",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )
    # else:
    #     from llama_index.embeddings import HuggingFaceEmbedding
    #     text_embedder = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")
    
    # Service Context for smaller LLM
    service_context_small = ServiceContext.from_defaults(
            llm=llm_small, embed_model=text_embedder,
        )

    # Service Context
    service_context = ServiceContext.from_defaults(
            llm=llm, embed_model=text_embedder,
        )
    
    ####################################
    # Create a list of task query engines for care recommendation
    print('='*50)
    print('Creating task query engines')
    print('='*50)
    task_query_engines_list = []
    task_name_list = ['Schedule of Clinical Visits',
                        'Cancer Surveillance or Other Recommended Tests',
                        'Possible late and long-term effects of cancer treatment',
                        'Other issues',
                        'Lifestyle and behavior',
                        'Helpful resources',
                        ]


    for task_name in task_name_list:
        print('Loading task knowledge base for task:',task_name)
        task_context = load_knowledge_base(f'{knowledge_path}/{task_name}',service_context)
        print(f'Creating query engine for task: {task_name}')
        task_query_engine = create_query_engine(vector_index = task_context, 
                                                                service_context = service_context,
                                                                top_K = 15,#100 - > for refined knowledge base,#10 -> for normal,
                                                                response_mode='compact')
        # print(task_query_engine.query(f'What are the recommended {task_name}?'))
        task_query_engines_list.append(task_query_engine)
        print(f'Created query engine for task: {task_name}')


    ############################################
        #       General Information   #
    ############################################
    
    print('='*50)
    print('Extracting General Information for Patient')
    print('='*50)
    start_time = time.time()
    
    # Convert patient data to list
    ### This is for clinical notes but need to change based on the patient data type
    patient_text_list = patient_data.split('\n') 
    general_info_query_engine = treatment_summary_query_engine(patient_text_list,
                                                                    service_context_small, 
                                                                    M=5,
                                                                    response_mode="compact")
    #one stage
    general_prompt = get_general_info_prompt(patient_data)
    # For each required information use RAG to retrieve the information and store in a dict
    general_dict = {'General Information':{}}
    
    for i in range(len(general_prompt)):
            general_info_key = general_prompt[i].split('\n\n')[-1].strip()
            general_dict['General Information'][f'{general_info_key}'] = str(general_info_query_engine.query(general_prompt[i]))

    general_info_time = time.time() - start_time
    time_dict['General Information'] = general_info_time
    
    ############################################
    #       Treatment summary generation    #
    ############################################
    print('='*50)
    print(f'Extracting Treatment Summary for Patient')
    print('='*50)
    #Create query engine for patient
    treatment_sum_query_engine = treatment_summary_query_engine(patient_text_list,
                                                                    service_context, 
                                                                    M=100,
                                                                    response_mode="compact")
    # List of tasks for treatment summary
    task_list = ['Diagnosis',
                'Treatment Completed',
                'Names of Agents used in Completed Treatments',
                'Persistent symptoms or side effects at completion of treatment',
                'Treatment Ongoing and Side Effects']
    
    for task_name in task_list:
        print(f'Retrieving {task_name} information')
        # Retrieve important information from patient data for task
        task_response = treatment_sum_query_engine.query(task_name)
        # Combine all the retrieved information into a single string
        relevant_patient_text = get_relevant_patient_text(task_response)

        # Get prompts for task in treatment summary
        treatment_summarizer_prompt = get_treatment_summarizer_prompts(task_name,relevant_patient_text)
        # Generate response for  task in treatment summary
        treatment_summary = llm.complete(treatment_summarizer_prompt)

        #Convert to json and append to dict
        treatment_summary_json = str(treatment_summary).split('{', 1)[1].strip()
        treatment_summary_json = '{' + treatment_summary_json.rsplit('}', 1)[0] + '}'
        treatment_summary_json = json.loads(treatment_summary_json)
        
        treatment_sum_dict['Treatment Summary'][f'{task_name}'] = treatment_summary_json[f'{task_name}']
        treatment_sum_dict['Relevant_patient_text'][f'{task_name}'] = relevant_patient_text

    treatment_sum_time = time.time() - start_time - general_info_time
    time_dict['Treatment Summary'] = treatment_sum_time
    
    ############################################
    #       Follow-up Care plan generation    #
    ############################################
    print('='*50)
    print(f'Generating Follow-up Care Plan for Patient')
    print('='*50)
    cancer_type = treatment_sum_dict['Treatment Summary']['Diagnosis']['Cancer type']
    # follow_up_care_plan['cancer_type'] = cancer_type
    # follow_up_care_plan['patient_data'] = patient_data
    task_name_list = ['Schedule of Clinical Visits',
                    'Cancer Surveillance or Other Recommended Tests',
                    'Possible late and long-term effects of cancer treatment',
                    'Other issues',
                    'Lifestyle and behavior',
                    'Helpful resources',
                    ]
    
    for task_name in task_name_list:
        print(f'Generating Follow-up Care Plan for Task: {task_name}')
        task_prompt, patient_prompt = get_care_prompts(task_name = task_name,
                                                cancer_type = cancer_type,
                                                patient_text = patient_data)
            
        #Get index of the task name in the list
        task_index = task_name_list.index(task_name)
        # Get query engine for the task
        patient_query_engine = task_query_engines_list[task_index]
        
        # Get care plan
        patient_care_recommend, patient_care_recommend_context = get_care_recommendation_2stage_patient_query(patient_query_engine,
                                                                                                            patient_prompt
                                                                )
        # Extract json from response
        patient_care_recommend_text, patient_care_recommend_json = extract_json_text_from_response(patient_care_recommend)
        # flag_except = 1
            # except:
            #     print('Exception occured. Retrying...')
            #     flag_except = 0
        # get main key name from json
        main_key = list(patient_care_recommend_json.keys())[0]
        if main_key != task_name:
            print(f'Warning: Main key {main_key} does not match task name {task_name}. Correcting...')
            patient_care_recommend_json ={f'{task_name}':patient_care_recommend_json}



        # Add to the dict
        follow_up_care_plan[f'{task_name}'] = {'recommendation':patient_care_recommend_json,
                                        'context':patient_care_recommend_context}

    follow_up_care_plan_time = time.time() - start_time - general_info_time - treatment_sum_time
    time_dict['Follow-up Care Plan'] = follow_up_care_plan_time
    
    ############################################
    #       Rectify Follow-up Care Plan        #
    ############################################
    print('='*50)
    print(f'Rectifying Follow-up Care Plan for Patient')
    print('='*50)
    
    for task_name in task_name_list:
        print(f'Rectifying recommendations for task: {task_name}')
        patient_care_recommend_json = follow_up_care_plan[task_name]['recommendation']
        patient_care_recommend_context = follow_up_care_plan[task_name]['context']  
        
        rect_recommend_json, removed_recommend_json = rectifier(patient_care_recommend_json,
                                                                            patient_care_recommend_context,
                                                                            patient_data,
                                                                            llm_rect,
                                                                            task_name, 
                                                                            num_iter = rect_iter,print_verbose=False)
    
        follow_up_care_plan_rect[f'{task_name}'] = {'recommendation':rect_recommend_json,
                                                    'context':patient_care_recommend_context}

        removed_care_recommendations[f'{task_name}'] = removed_recommend_json
        
        print(f'Rectification done for task: {task_name}')
    
    rectification_time = time.time() - start_time - general_info_time - treatment_sum_time - follow_up_care_plan_time
    time_dict['Rectification'] = rectification_time
    time_dict['Total'] = time.time() - start_time
    
    return general_dict, treatment_sum_dict, follow_up_care_plan, follow_up_care_plan_rect, removed_care_recommendations, time_dict



if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080, debug=True)
