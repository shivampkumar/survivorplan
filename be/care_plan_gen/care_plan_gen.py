import json
from llama_index.core import Document
from llama_index.core import StorageContext, load_index_from_storage

from utils.rag_utils import create_vector_index, create_query_engine
from utils.rag_utils import patient_care_query_engine, create_task_context_dict


# def extract_keys_values(d, path=''):
#     """Recursively extract keys and values from a nested dictionary and format as a string."""
#     output = ""
#     for k, v in d.items():
#         new_path = f"{path} | {k}" if path else k  # Prepare the key path
#         if isinstance(v, dict):
#             # Recursively call for nested dictionaries
#             output += extract_keys_values(v, new_path)
#         else:
#             # Append the key and value as a string
#             output += f"{new_path}: {v}\n"
#     return output

def extract_keys_values(d, path=''):
    """Recursively extract keys and values from a nested dictionary, converting lists to strings, and format as a string."""
    output = ""
    for k, v in d.items():
        new_path = f"{path}.{k}" if path else k  # Prepare the key path
        if isinstance(v, dict):
            # Recursively call for nested dictionaries
            output += extract_keys_values(v, new_path)
        elif isinstance(v, list):
            # Convert list to string and append
            list_as_string = ', '.join(map(str, v))  # Convert each item in the list to string and join with comma
            output += f"{new_path}: [{list_as_string}]\n"
        else:
            # Append the key and value as a string
            output += f"{new_path}: {v}\n"
    return output

def create_knowledge_base(knowledge_files,service_context):
    '''
    Creating knowledge base from processed guidelines and vectorstoreindex 
    Given the list of processed guidelines as json files 
    and service context (embedding model and llm, etc), create a vector store index
    
    Args:
        knowledge_files: list of json files containing the processed guidelines
        service_context: llamaindex service context containing the embedding model and llm
    Returns:
        guideline_vector_index: vector store index for the processed guidelines
    '''
    # Load the processed guidelines from the json files
    documents = []
    for file in knowledge_files:
        with open(file) as f:
            data = json.load(f)
            for item in data:
                documents.append(item)

    documents = [Document(**doc) for doc in documents]

    # print(documents)
    # Create a vector store index
    guideline_vector_index = create_vector_index(documents, service_context)    

    return guideline_vector_index


def load_knowledge_base(knowledge_path,service_context):
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=f"{knowledge_path}")

    # load index
    storage_index = load_index_from_storage(storage_context, service_context=service_context)
    return storage_index


def get_care_recommendation_2stage(guideline_vector_index,
                            service_context,
                            task_prompt,
                            patient_prompt,
                            top_K_task=10,
                            top_K_patient=3,
                            task_response_mode="no_text",
                            care_recommend_response_mode="compact",
                            ):
    '''
    Two-stage retrieval and generation of follow-up care recommendation.
    
    Stage 1:    Given the vector store index for the processed guidelines, service context,
                creates a query engine and retrieves top {top_K_task} context relevant to the task.
                Then creates a intermediate knowledge base using the task context.
    Stage 2:    Given the intermediate knowledge base, creates a query engine and retrieves 
                top {top_K_patient} context relevant to the patient and the task. Then use those context 
                for care recommendation.
    
    Args:
        guideline_vector_index: vector store index for the processed guidelines
        service_context: llamaindex service context containing the embedding model and llm
        task_prompt: task prompt for the task
        patient_prompt: patient prompt for the patient
        top_K_task: number of context to retrieve for the task
        top_K_patient: number of context to retrieve for the patient
        task_response_mode: response mode for the task context retrieval
        care_recommend_response_mode: response mode for the care recommendation generation
    Returns:
        patient_care_recommend: care recommendation for the patient
        patient_care_recommend_context_dict: context retrieved for the patient
        task_context_dict: context retrieved for the task
        if task_response_mode != "no_text":
            task_response: response for the task context retrieval
    '''

    # Initialize the task query engine, configure task retriever to extract top {top_K_task} context relevant to the task
    task_context_query_engine = create_query_engine(vector_index = guideline_vector_index, 
                                                             service_context = service_context,
                                                             top_K = top_K_task,
                                                             response_mode=task_response_mode)
    
    ### Stage 1: Task Context Retrieval
    # Retrieve necessary task context from the knowledge base for the given task
    if task_response_mode != "no_text":
        task_context = task_context_query_engine.query(task_prompt)
        task_response = task_context.response
        task_context = task_context.source_nodes
    else:
        task_context = task_context_query_engine.query(task_prompt).source_nodes

    
    # Create a query engine to retrieve and generate care recommendation for the patient. Knowledge base is the task context
    # configure retriever to extract top {top_K_patient} context relevant to the patient
    patient_query_engine = patient_care_query_engine(task_context,service_context, M=top_K_patient,response_mode=care_recommend_response_mode)

    ### Stage 2: Patient Context Retrieval and Care Recommendation Generation
    patient_care_recommend = patient_query_engine.query(patient_prompt)

    # Get context retieved for this specific patient
    patient_care_recommend_context = patient_care_recommend.source_nodes

    # Convert context to dictionary
    task_context_dict = create_task_context_dict(task_context)
    patient_care_recommend_context_dict = create_task_context_dict(patient_care_recommend_context)
    # return patient_care_recommend, patient_care_recommend_context, task_context

    if task_response_mode != "no_text":
        return patient_care_recommend, patient_care_recommend_context_dict, task_context_dict, task_response

    return patient_care_recommend, patient_care_recommend_context_dict, task_context_dict



############ 1 stage RAG ############
def get_care_recommendation_1stage(guideline_vector_index,
                            service_context,
                            patient_prompt,
                            top_K_patient=3,
                            care_recommend_response_mode="compact",
                            ):
    '''
    One-stage retrieval and generation of follow-up care recommendation.
    Given the vector store index for the processed guidelines, service context,
    creates a query engine and retrieves top {top_K_patient} context relevant to the patient.
    Then use those context for care recommendation.

    Args:
        guideline_vector_index: vector store index for the processed guidelines
        service_context: llamaindex service context containing the embedding model and llm
        patient_prompt: patient prompt for the patient
        top_K_patient: number of context to retrieve for the patient
        care_recommend_response_mode: response mode for the care recommendation generation
    Returns:
        patient_care_recommend: care recommendation for the patient
        patient_care_recommend_context_dict: context retrieved for the patient
    '''

    #Stage 1: Patient Context Retrieval and Care Recommendation Generation
    # Create a query engine to retrieve and generate care recommendation for the patient. Knowledge base is the preprocessed guidelines
    patient_query_engine = create_query_engine(vector_index = guideline_vector_index, 
                                                             service_context = service_context,
                                                             top_K = top_K_patient,
                                                             response_mode=care_recommend_response_mode)
 
    patient_care_recommend = patient_query_engine.query(patient_prompt)

    # Get context retieved for this specific patient
    patient_care_recommend_context = patient_care_recommend.source_nodes

    # Convert context to dictionary
    patient_care_recommend_context_dict = create_task_context_dict(patient_care_recommend_context)
    # return patient_care_recommend, patient_care_recommend_context, task_context



    return patient_care_recommend, patient_care_recommend_context_dict


def extract_json_text_from_response(response):
    '''
    Given the response from the query engine, extract the json part and the text part separately and
    convert the json part to a dictionary
    Args:
        response: response from the query engine
    Returns:
        text_part: text part of the response
        json_part: json part of the response
    '''
    # print(response.response)
    # split the response into two parts one is the response and the other is the json. split based on first occurance of '{'
    # text_part = response.response.split('{', 1)[0][:-1]
    # json_part = response.response.split('{', 1)[1].strip()
    if 'JSON Response:' not in response.response:
        text_part = response.response.split('{', 1)[0]
        json_part = '{'+response.response.split('{', 1)[1].strip()
    else:
        text_part = response.response.split('JSON Response:', 1)[0][:-1]
        json_part = response.response.split('JSON Response:', 1)[1].split('\n',1)[1].strip()
    
    json_part = json_part.rsplit('}', 1)[0].strip() + '}'
    # print(json_part)          
    json_part = json.loads(json_part)
    # print(json_part)

    return text_part, json_part


def convert_synthea_to_text(patient_data):
    '''
    Function to convert the synthea tabular data to text
    Args:
        patient_data: tabular data for the patient
    Returns:
        patient_text: text for the patient
    '''
    # Convert the synthea data to text
    patient_text = ''
    for col in patient_data.index:
        try:
            if "not given" in str(patient_data[col]):
                continue
            patient_text += col +' : '
            patient_text += str(patient_data[col]) + ' || '
            # print(f'text: {text}')
        except:
            continue
    return patient_text

def get_relevant_patient_text(response):
    '''
    Given the response from the query engine, extract the relevant patient text from the source nodes
    and return it as a text
    Args:
        response: response from the query engine
    Returns:
        relevant_patient_text: text for the patient
    '''
    relevant_patient_text = ''
    for i in range(len(response.source_nodes)):
        # print(response.source_nodes[i].text)
        relevant_patient_text += response.source_nodes[i].text + ' || '
    return relevant_patient_text



def get_care_recommendation_2stage_patient_query(patient_query_engine,
                            patient_prompt,
                            ):
    '''
    '''
    ### Stage 2: Patient Context Retrieval and Care Recommendation Generation
    patient_care_recommend = patient_query_engine.query(patient_prompt)

    # Get context retieved for this specific patient
    patient_care_recommend_context = patient_care_recommend.source_nodes

    # Convert context to dictionary
    # task_context_dict = create_task_context_dict(task_context)
    patient_care_recommend_context_dict = create_task_context_dict(patient_care_recommend_context)
    # return patient_care_recommend, patient_care_recommend_context, task_context



    return patient_care_recommend, patient_care_recommend_context_dict, 