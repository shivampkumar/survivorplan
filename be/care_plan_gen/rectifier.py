import numpy as np


def extract_care_statements_from_json(response_json,task_name):
    '''
    Given a response as json, extract the care plan related statements from the response
    Args:
        response_json (json): Response as json
        task_name (str): Name of the task
    Returns:
        ans_statements_list (list): List of statements extracted from the response
    '''
    
    ans_statements_list = []

    for i in range(len(response_json[f'{task_name}'])):
        ans_statement = ''
        for _,v in enumerate(response_json[f'{task_name}'][i]):
            ans_statement += str(v) + ': ' + str(response_json[f'{task_name}'][i][v]) + '\n'

        ans_statements_list.append(ans_statement)

    return ans_statements_list, task_name




def convert_patient_context_to_text(patient_context):
    '''
    Given a patient context as a list of dictionaries, convert it to text
    Args:
        patient_context (list): List of dictionaries
    Returns:
        patient_context_text (str): Patient context as text in the format of Metadata: {metadata} || Text: {text} \n ------------------------ \n\n 
    '''
    
    patient_context_text = ''
    for i in range(len(patient_context)):
        patient_context_text += 'Metadata: '
        patient_context_text +=' File name '+ patient_context[i]['metadata']['file_name'] 
        patient_context_text +=' Page label ' + patient_context[i]['metadata']['page_label']
        patient_context_text +=' || Text: ' + patient_context[i]['text'] + '\n'
        patient_context_text += '------------------------\n\n'

    return patient_context_text

def rectifier_recommendation_faithfulness(ans_statements_list, patient_context_text,patient_data_text, llm,task_name, print_verbose=False):


    verdict_list = []
    for i in range(len(ans_statements_list)):
        # prompt = f"\
        #             Context information retrieved for patient and task of recommendating {task_name} is given below.\n\
        #             --------------------- \n\
        #             {patient_context_text} \n \
        #             ---------------------. \n\n \
        #             Given the retreived context information, determine whether the following recommendation for {task_name} is supported by the information present in the context.\
        #             Provide an explanation for the decision before arriving at the verdict (Yes/No). \n\n\
        #             recommendation: \n \
        #             {ans_statements_list[i]} \n \
        #             Give the response in the following format and do not deviate from the specified format: \n\n \
        #                 Verdict: <Yes/No> \n \
        #                 Explanation: <explanation> "

        prompt = f"\
                    Patient information is given below.\n\
                    --------------------- \n\
                    {patient_data_text} \n \
                    ---------------------. \n\n \
                    Context information retrieved for the above patient and task of recommendating {task_name} is given below.\n\
                    --------------------- \n\
                    {patient_context_text} \n \
                    ---------------------. \n\n \
                    Given the patient information and retreived context information, determine whether the following recommendation for {task_name} is supported by the information present in patient and context information and not hallucinated.\
                    Provide an explanation for the decision before arriving at the verdict (Yes/No). \n\n\
                    recommendation: \n \
                    {ans_statements_list[i]} \n \
                    Give the response in the following format and do not deviate from the specified format: \n\n \
                        Verdict: <Yes/No> \n \
                        Explanation: <explanation> "
        
        verdict_response = llm.complete(prompt)
        if print_verbose:
            print(verdict_response)

        verdict = str(verdict_response).split('Verdict')[-1].split('Explanation')[0]
        if 'Yes' in verdict:
            verdict_list.append(1)
        elif 'No' in verdict:
            verdict_list.append(0)
        else:
            flag = 0
            print('Exception occured')
            while flag == 0:
                verdict_response = llm.complete(prompt)
                verdict = str(verdict_response).split('Verdict')[-1].split('Explanation')[0]
                if 'Yes' in verdict:
                    verdict_list.append(1)
                    flag = 1
                elif 'No' in verdict:
                    verdict_list.append(0)
                    flag = 1
            print('Exception resolved')
        
        


    return verdict_list

def rectifier_patient_relevance(ans_statements_list,patient_context_text, patient_data_text, llm,task_name, print_verbose=False):
    
    # print(statement_str)
    verdict_list = []
    for i in range(len(ans_statements_list)):
        prompt = f"\
                    Patient information is given below.\n\
                    --------------------- \n\
                    {patient_data_text} \n \
                    ---------------------. \n\n \
                    Context information retrieved for above patient and task of recommendating {task_name} is given below.\n\
                    --------------------- \n\
                    {patient_context_text} \n \
                    ---------------------. \n\n \
                    Given the patient information and retreived context information, determine whether the following recommendation for {task_name} is relevant to the given patient and supported by given context information.\
                    Provide an explanation for the decision before arriving at the verdict (Yes/No). \n\n\
                    recommendation: \n \
                    {ans_statements_list[i]} \n \
                    Give the response in the following format and do not deviate from the specified format: \n \
                    Verdict: <Yes/No> \n \
                    Explanation: <explanation> \n "
        
        verdict_response = llm.complete(prompt)
        if print_verbose:
            print(verdict_response)

        verdict = str(verdict_response).split('Explanation')[0]
        if 'Yes' in verdict:
            verdict_list.append(1)
        elif 'No' in verdict:
            verdict_list.append(0)
        else:
            flag = 0
            print('Exception occured')
            while flag == 0:
                verdict_response = llm.complete(prompt)
                verdict = str(verdict_response).split('Explanation')[0]
                if 'Yes' in verdict:
                    verdict_list.append(1)
                    flag = 1
                elif 'No' in verdict:
                    verdict_list.append(0)
                    flag = 1
            print('Exception resolved')
        
    return verdict_list

def rectifier(response_json,context, patient_data_text, llm,task_name, num_iter = 10,print_verbose=False):
    '''
    Given a care recommendation from the query engine, rectify the recommendation based on answer faithfulness.
    Args:
        response_json (json): Response as json
        context (list): List of dictionaries containing context relevant to the patient and task
        patient_data_text (str): Patient data as text
        llm: Language model (llamaindex AzureOpenAI object)
        task_name (str): Name of the task
        num_iter (int): Number of iterations to run the rectifier
        print_verbose (bool): Whether to print the response from the language model
    Returns:
        rect_response_json (json): Rectified response as json
        all_recom_faithfulness_list (list): List of faithfulness scores for each recommendation
    '''

    # Extract the care statements from answer in json format given by llm
    ans_statements_list, task_name = extract_care_statements_from_json(response_json, task_name)

    # Convert extracted patint context to text in the format of Metadata: {metadata} || Text: {text} \n ------------------------ \n\n
    patient_context_text = convert_patient_context_to_text(context)

    # Get scores for faithfulness and patient relevance
    all_recom_faithfulness_list =[]
    all_recom_patient_relevance_list = []

    for i in range(num_iter):
        all_recom_faithfulness_list.append(rectifier_recommendation_faithfulness(ans_statements_list = ans_statements_list,
                                                                             patient_context_text= patient_context_text,
                                                                                patient_data_text=patient_data_text,
                                                                             llm = llm,
                                                                             task_name= task_name,
                                                                             print_verbose=print_verbose))
        # all_recom_patient_relevance_list.append(rectifier_patient_relevance(ans_statements_list = ans_statements_list,
        #                                                                      patient_context_text= patient_context_text,
        #                                                                 patient_data_text=patient_data_text,
        #                                                                 llm=llm,
        #                                                                 task_name=task_name,
        #                                                                 print_verbose=print_verbose))
        

        # all_recom_faithfulness_list.append(recom_faithfulness_list)
        # all_recom_patient_relevance_list.append(recom_patient_relevance_list)

    
    # print('all_recom_faithfulness_list: ',all_recom_faithfulness_list)
    # print('all_recom_patient_relevance_list: ',all_recom_patient_relevance_list)
    

    # Get the average scores for faithfulness and patient relevance in axis
    all_recom_faithfulness_list = np.array(all_recom_faithfulness_list)
    # all_recom_patient_relevance_list = np.array(all_recom_patient_relevance_list)

    if all_recom_faithfulness_list.shape[0] >1:
        all_recom_faithfulness_list = np.sum(all_recom_faithfulness_list,axis=0)/num_iter
        # all_recom_patient_relevance_list = np.sum(all_recom_patient_relevance_list,axis=0)/num_iter
    else:
        all_recom_faithfulness_list = all_recom_faithfulness_list.flatten()
        # all_recom_patient_relevance_list = all_recom_patient_relevance_list.flatten()


    # get list of indiceswith higher score in response json
    select_indices = []
    removed_indices = []
    for i in range(len(all_recom_faithfulness_list)):
        if all_recom_faithfulness_list[i] < 0.6:# or all_recom_patient_relevance_list[i] < 0.6:
            removed_indices.append(i)
            continue
            
        select_indices.append(i)
    
    # remove the indices from response json
    rect_response_json = {}
    rect_response_json[task_name] = [response_json[task_name][i] for i in select_indices]

    removed_recom_json = {}
    removed_recom_json[task_name] = [response_json[task_name][i] for i in removed_indices]

    return rect_response_json, removed_recom_json#all_recom_faithfulness_list, all_recom_patient_relevance_list

