from llama_index.core import Document, ServiceContext, VectorStoreIndex
from llama_index.core  import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


def create_vector_index(documents,service_context):
    '''
    Create a vector index from the given documents and llms 
    '''
    # Create a service context for embedding
    # service_context = ServiceContext.from_defaults(
    #     llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
    # )

    # Create a vector store index
    vector_index = VectorStoreIndex.from_documents(
        documents=documents,service_context=service_context)
    return vector_index


def create_query_engine(vector_index,service_context, top_K, response_mode="no_text"):
    '''
    Create a query engine for the given vector index and top_K
    '''
    # Create a service context for embedding
    # service_context = ServiceContext.from_defaults(
    #     llm=llm, embed_model="local:BAAI/bge-small-en-v1.5"
    # )

    # configure context retriever to extract top N context relevant to the task 
    context_retreiver = VectorIndexRetriever(
                                    index=vector_index,
                                    similarity_top_k=top_K,
                                )

    # configure task response synthesizer
    response_synthesizer = get_response_synthesizer(
        response_mode=response_mode,
        service_context=service_context,)

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=context_retreiver,
        response_synthesizer=response_synthesizer,)
    # query_engine = vector_index.as_query_engine(top_K=top_K,response_mode=response_mode,service_context=service_context)
    
    return query_engine

def patient_care_query_engine(task_context,service_context, M=3,response_mode="compact"):
    '''
    Create a query engine to retrieve and generate care plan for patients

    Args:
        task_context: (Knowledge base) retrieved task context for the specific care task 
        llm: language model
        M: Configure retriever to extract top M context relevant to the patient
    '''

    # Create a document base from the task context
    task_context_docs = create_task_context_doc_base(task_context)

    # Create a vector store index
    task_vector_index = create_vector_index(task_context_docs, service_context)

    # Create a query engine to retrieve answers from the patient
    patient_query_engine = create_query_engine(vector_index = task_vector_index,
                                                                    service_context = service_context,
                                                                    top_K = M,
                                                                    response_mode=response_mode)
    
    return patient_query_engine




def create_task_context_dict(task_context):
    # Create a dictionary with only the text and metadata extracted from the task_context.source_nodes 
    task_context_dict = []
    for i in range(len(task_context)):
        context_i = {"metadata": {'page_label': task_context[i].metadata['page_label'],'file_name': task_context[i].metadata['file_name']},
                    'text': task_context[i].text}
        task_context_dict.append(context_i)
    return task_context_dict


# Create a document base from the task context
def create_task_context_doc_base(task_context):
    task_context_docs = []
    for i in range(len(task_context)):
        task_context_docs.append(Document(text=task_context[i].text,metadata=task_context[i].metadata))
    return task_context_docs




#### For patient data
def create_patient_doc_base(patient_text_list):
    patient_docs = []
    for i in range(len(patient_text_list)):
        if patient_text_list[i] != '':
            patient_docs.append(Document(text=patient_text_list[i]))
    return patient_docs

def treatment_summary_query_engine(patient_text_list,service_context, M=3,response_mode="compact"):
    '''
    Create a query engine to retrieve and generate care plan for patients

    Args:
        task_context: (Knowledge base) retrieved task context for the specific care task 
        llm: language model
        M: Configure retriever to extract top M context relevant to the patient
    '''

    # Create a document base from the task context
    patient_doc_base = create_patient_doc_base(patient_text_list)
    # print('patient_doc_base',patient_doc_base)

    # Create a vector store index
    patient_vector_index = create_vector_index(patient_doc_base, service_context)

    # Create a query engine to retrieve answers from the patient
    query_engine = create_query_engine(vector_index = patient_vector_index,
                                                                    service_context = service_context,
                                                                    top_K = M,
                                                                    response_mode=response_mode)
    
    return query_engine


def dict_to_text_file(d, file_name, indent=0):
    """
    Write a nested dictionary (which may contain lists with dictionaries) to a text file.
    Indentation represents the hierarchy.

    :param d: The nested dictionary to write to the file.
    :param file_name: The name of the text file to be created.
    :param indent: The current indentation level (used for recursion).
    """
    with open(file_name, 'w') as file:
        def write_item(item, indent):
            if isinstance(item, dict):
                for key, value in item.items():
                    file.write('    ' * indent + str(key) + ':')
                    if isinstance(value, (dict, list)):
                        file.write('\n')
                        write_item(value, indent + 1)
                    else:
                        file.write(' ' + str(value) + '\n')
            elif isinstance(item, list):
                for element in item:
                    write_item(element, indent)

        write_item(d, indent)