


def get_care_prompts(task_name,cancer_type,patient_text,treatment_text = None):
    '''
    Obtain the prompts for the given task and patient data for follow-up care recommendation
    Args:
        task_name: name of the task should be one of the following
                   ['treatment summary', 
                   'Schedule of Clinical Visits', 
                   'Cancer Surveillance or Other Recommended Tests',
                   'Possible late and long-term effects of cancer treatment',
                   'Other issues',
                   'Lifestyle and behavior',
                   'Helpful resources']
        cancer_type: type of cancer
        patient_text: patient data in text format
    Returns:
        task_prompt: prompt for the task
        patient_prompt: prompt for the patient data
        if task_name is 'treatment summary':
            patient_prompt is not returned
            treatment_summarizer_prompt: prompt for the treatment summarizer
    '''

    
    if task_name == 'Schedule of Clinical Visits':
        # Prompt for the task: Schedule of Clinical Visits
        task_prompt = f'Recommend a schedule of clinical visits for cancer survivors.'#{cancer_type}
        # Prompt for patient care recommendation for given patient data and task
        response_format = '{"Schedule of Clinical Visits":[{"Visit type":< coordinating provider >,\
            "When / how often":< when to visit or frequency of visits >\
            "Explanation": < explanation for the recommendation >\
            "File names": <list of file name>\
            "Page labels": <list of page label>},\
            {"Visit type":< coordinating provider >,\
            "When / how often":< when to visit or frequency of visits >\
            "Explanation": < explanation for the recommendation >\
            "File names": <list of file name>\
            "Page labels": <list of page label>}, ...\
                ]}'
        patient_prompt = f'\
                        Patient information is below.\n\
                        --------------------- \n\
                        {patient_text} \n \
                        ---------------------. \n \
                        Given the patient information of a {cancer_type} survivor, recommend a schedule of clinical visits for their follow-up care.\
                        Provide explanation for each recommendation and specifically mention why this patient requires this recommendation in the explanation.\n \
                        Also, provide the list of metadata (file names and page labels) of information present in the context which supports each recommendation. Do not repeat the same recommendation.\n\n\
                        Initially provide text output and then convert the response into the following JSON format. \n\n \
                            {response_format} \n\n \
                        Provide this JSON response at the end of the output in the next line after stating "JSON Response:". Do not deviate from these instructions. \n \
                        '
        return task_prompt, patient_prompt
    
    if task_name == 'Cancer Surveillance or Other Recommended Tests':
        # Prompt for the task: Cancer Surveillance or Other Recommended Tests
        task_prompt = f'Recommend cancer surveillance and other recommended tests for cancer survivors.'#{cancer_type}

        response_format = '{"Cancer Surveillance or Other Recommended Tests":[{"Test type":< recommended test >,\
            "Coordinating provider":< coordinating provider >,\
            "When / how often":< frequency of tests >,\
            "Explanation": < explanation for the test recommendation >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>},\
            {"Test type":< recommended test >,\
            "Coordinating provider":< coordinating provider >,\
            "When / how often":< frequency of tests >,\
            "Explanation": < explanation for the test recommendation >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>}, ...\
                ]}'
        # Prompt for patient care recommendation for given patient data and task
        patient_prompt = f'\
                        Patient information is below.\n\
                        --------------------- \n\
                        {patient_text} \n \
                        ---------------------. \n \
                        Given the patient information of a {cancer_type} survivor, recommend a set of tests for cancer surveillance during their follow-up care. \
                        Provide reasoning/explanation for each recommendation and specifically mention which patient information and retrieved context information is the reason behind this recommendation.\n \
                        Also, provide the list of metadata (file names and page labels) of information present in the context which supports each recommendation. Do not repeat the same recommendation.\n\n\
                        Initially provide text output and then convert the response into the following JSON format. \n\n \
                            {response_format} \n\n \
                        Provide this JSON response at the end of the output in the next line after stating "JSON Response:". Do not deviate from these instructions. \n \
                        '
        return task_prompt, patient_prompt
    
    if task_name == 'Possible late and long-term effects of cancer treatment':
        # Prompt for the task: Possible late and long-term effects of cancer treatmen -->could be used for evaluation as the effects are fixed
        task_prompt = f'Suggest possible late and long-term effects of cancer treatment'
        
        response_format = '{"Possible late and long-term effects of cancer treatment":[{"Treatment effect": < possible treatment effect >,\
            "Explanation": < explanation for the suggested treatment effect >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>},\
            {"Treatment effect": < possible treatment effect >,\
            "Explanation": < explanation for the suggested treatment effect >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>}, ...\
            ]}'
        # Prompt for patient care recommendation for given patient data and task
        if treatment_text != None:
            patient_prompt = f'\
                            The following are the diagnosis, completed and ongoing treatments information of the patient\n\
                            --------------------- \n\
                            {treatment_text} \n \
                            ---------------------. \n \
                            Given the patient information and treatment details of a {cancer_type} survivor, suggest possible late and long-term effects of the treatments they might face during follow-up care.\
                            Provide reasoning/explanation for each suggestion and specifically mention which patient information and retrieved context information is the reason behind this suggestion.\n \
                            Also, provide the list of metadata (file names and page labels) of information present in the context which supports each suggestion. Do not repeat the same suggestion.\n\n\
                            Initially provide text output and then convert the response into the following JSON format. \n\n \
                                {response_format} \n\n \
                            Provide this JSON response at the end of the output in the next line after stating "JSON Response:". Do not deviate from these instructions. \n \
                            '
                            
                            
                            
                            
                            
        
        else:
            patient_prompt = f'\
                            Patient information is below.\n\
                            --------------------- \n\
                            {patient_text} \n \
                            ---------------------. \n \
                            Given the patient information of a {cancer_type} survivor, suggest possible late and long-term effects of cancer treatment they might face during follow-up care.\
                            Provide reasoning/explanation for each suggestion and specifically mention which patient information and retrieved context information is the reason behind this suggestion.\n \
                            Also, provide the list of metadata (file names and page labels) of information present in the context which supports each suggestion. Do not repeat the same suggestion.\n\n\
                            Initially provide text output and then convert the response into the following JSON format. \n\n \
                                {response_format} \n\n \
                            Provide this JSON response at the end of the output in the next line after stating "JSON Response:". Do not deviate from these instructions. \n \
                            '
        return task_prompt, patient_prompt
    
    if task_name == 'Other issues':
        # Prompt for the task: Other issues
        task_prompt = f'Suggest possible issues that cancer survivors may experience'
        response_format = '{"Other issues":[{"Issue":< suggested issue >,\
            "Explanation": < explanation for the suggestion of the issue >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>},\
            {"Issue":< suggested issue >,\
            "Explanation": < explanation for the suggestion of the issue >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>}, ...\
                ]}'
        
        patient_prompt = f'\
                Patient information is below.\n\
                --------------------- \n\
                {patient_text} \n \
                ---------------------. \n \
                Given the patient information of a {cancer_type} survivor, suggest possible other issues that the patient might face during follow-up care.\
                Provide reasoning/explanation for each suggestion and specifically mention which patient information and retrieved context information is the reason behind this suggestion.\n \
                Also, provide the list of metadata (file names and page labels) of information present in the context which supports each suggestion. Do not repeat the same suggestion.\n\n\
                Initially provide text output and then convert the response into the following JSON format. \n\n \
                    {response_format} \n\n \
                Provide this JSON response at the end of the output in the next line after stating "JSON Response:" \n. Do not deviate from these instructions. \
                '
        return task_prompt, patient_prompt
    
    if task_name == 'Lifestyle and behavior':
        # Prompt for the task: Lifestyle and behavior recommendation
        task_prompt = f'Recommend Lifestyle or behaviors for cancer survivors'
        response_format = '{"Lifestyle and behavior":[{"Lifestyle":< recommended lifestyle >,\
            "Explanation": < explanation for the lifestyle recommendation >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>},\
            {"Lifestyle":< recommended lifestyle >,\
            "Explanation": < explanation for the lifestyle recommendation >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>}, ...\
                ]}'
        # Prompt for patient care recommendation for given patient data and task
        patient_prompt = f'\
                        Patient information is below.\n\
                        --------------------- \n\
                        {patient_text} \n \
                        ---------------------. \n \
                        Given the patient information of a {cancer_type} survivor, recommend a number of lifestyle or behaviors for the given patient during follow-up care. \
                        Provide reasoning/explanation for each recommendation and specifically mention which patient information and retrieved context information is the reason behind this recommendation.\n \
                        Also, provide the list of metadata (file names and page labels) of information present in the context which supports each suggestion. Do not repeat the same recommendation.\n\n\
                        Initially provide text output and then convert the response into the following JSON format. \n\n \
                            {response_format} \n\n \
                        Provide this JSON response at the end of the output in the next line after stating "JSON Response:" \n. Do not deviate from these instructions.\
                        '
        return task_prompt, patient_prompt
    
    if task_name == 'Helpful resources':
        # Prompt for the task: Helpful resources
        task_prompt = f'Recommend helpful resources for {cancer_type} cancer survivors'
        response_format = '{"Helpful resources":[{"Resource":< recommended resource >,\
            "Explanation": < explanation for the resource recommendation >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>},\
            {"Resource":< recommended resource >,\
            "Explanation": < explanation for the resource recommendation >,\
            "File names": <list of file name>,\
            "Page labels": <list of page label>}, ...\
                ]}'
        # Prompt for patient care recommendation for given patient data and task
        patient_prompt = f'\
                        Patient information is below.\n\
                        --------------------- \n\
                        {patient_text} \n \
                        ---------------------. \n \
                        Given the patient information of a {cancer_type} survivor, recommend helpful resources for the patient during follow-up care.\
                        Provide reasoning/explanation for each recommendation and specifically mention which patient information and retrieved context information is the reason behind this recommendation.\n \
                        Also, provide the list of metadata (file names and page labels) of information present in the context which supports each suggestion. Do not repeat the same recommendation.\n\n\
                        Initially provide text output and then convert the response into the following JSON format. \n\n \
                            {response_format} \n\n \
                        Provide this JSON response at the end of the output in the next line after stating "JSON Response:" \n. Do not deviate from these instructions. \
                        '
        
        return task_prompt, patient_prompt
    

def get_treatment_summarizer_prompts(task_name,relevant_patient_text):
    '''
    Obtain the prompts for the given task and patient data for treatment summarizer (2 stage retrieval and generation)
    Args:
        task_name: name of the task should be one of the following
                        ['Diagnosis',
                        'Treatment Completed',
                        'Names of Agents used',
                        'Persistent symptoms or side effects at completion of treatment',
                        'Treatment Ongoing and Side Effects']
        relevant_patient_text: patient data in text format
        cancer_type: type of cancer
    Returns:
        treatment_summarizer_prompt: prompt for the treatment summarizer
    '''
    if task_name == 'Diagnosis':
        response_format = '{"Diagnosis": {"Cancer type": < cancer type >,\
            "Diagnosis Date": < diagnosis date >,\
            "Cancer stage": < cancer stage>\
            }\
            }'
        treatment_summarizer_prompt = f'\
                            Patient information is below.\n\
                            --------------------- \n\
                            {relevant_patient_text} \n \
                            ---------------------. \n \
                            Given the patient information extract following information on their treatment. Use only the given patient information and not prior information. \n\
                            If the information is not given in patient data specify not given. \n \
                            Provide the response in the following JSON format and do not deviate from the specified format. \n\n \
                            {response_format} \n\n \
                            Ensure to provide the response in a proper JSON format without indent with main key as {task_name} and provide it at the end of the response \n \
                            '
    if task_name == 'Treatment Completed':
        response_format = '{"Treatment Completed": {"Surgery": < Yes or No >,\
            "Surgery Date(s) (year)": < surgery date >,\
            "Surgical Procedure/location/findings": < surgical procedure, location and findings >,\
            "Radiation": < Yes or No >,\
            "Body area treated": < body area treated >,\
            "End Date (year)": < end date >,\
            "Systemic Therapy (Chemotherapy, hormonal therapy, other)": < Yes or No >\
            }\
            }'
            
        treatment_summarizer_prompt = f'\
                            Patient information is below.\n\
                            --------------------- \n\
                            {relevant_patient_text} \n \
                            ---------------------. \n \
                            Given the patient information extract following information on their treatment. Use only the given patient information and not prior information. \n\
                            If the information is not given in patient data specify not given. \n \
                            Provide the response in the following JSON format and do not deviate from the specified format. \n\n \
                            {response_format} \n\n \
                            Ensure to provide the response in a proper JSON format without indent with main key as {task_name} and provide it at the end of the response \n \
                            '
   
    if task_name == 'Names of Agents used in Completed Treatments':#'Names of Agents used':
        
        response_format = '{"Names of Agents used in Completed Treatments":[{"Agent 1": "< Name of the Agent used in Completed Treatment >", "End Date (year)": "< end date >"}, {"Agent 2": "< Name of the Agent used in Completed Treatment >", "End Date (year)": "< end date >"}, ...]}'
        treatment_summarizer_prompt = f'\
                            Patient information is below.\n\
                            --------------------- \n\
                            {relevant_patient_text} \n \
                            ---------------------. \n \
                            Given the patient information extract following information on the agents used for completed treatments. Use only the given patient information and not prior information. \n\
                            Only include the agents used in the completed treatment and not ongoing treatments. \n\
                            Example: if the end date is ongoing, ignore that treatment. \n\
                            If the information is not given in patient data specify not given. \n \
                            Provide the response in the following JSON format and do not deviate from the specified format. \n\n \
                            {response_format} \n\n \
                            Ensure to provide the response in a proper JSON format without indent with main key as {task_name} and provide it at the end of the response \n \
                            '

    if task_name == 'Persistent symptoms or side effects at completion of treatment':
        response_format = '{"Persistent symptoms or side effects at completion of treatment": {"Symptoms of side effects": < Yes or No >,\
            "Symptom or side effect types": < list of [ persistent symptom or side effect types ] >\
            }\
            }'
            
        treatment_summarizer_prompt = f'\
                            Patient information is below.\n\
                            --------------------- \n\
                            {relevant_patient_text} \n \
                            ---------------------. \n \
                            Given the patient information extract following information on their completed treatments. Use only the given patient information and not prior information. \n\
                            If the information is not given in patient data specify not given. \n \
                            Provide the response in the following JSON format and do not deviate from the specified format. \n\n \
                            {response_format} \n\n \
                            Ensure to provide the response in a proper JSON format without indent with main key as {task_name} and provide it at the end of the response \n \
                            '
    if task_name == 'Treatment Ongoing and Side Effects':
        response_format = '{"Treatment Ongoing and Side Effects": {"Need for ongoing (adjuvant) treatment for cancer": < Yes or No >,\
            "Ongoing treatment 1": < list of [ ongoing treatment, planned duration , possible side effects ] >,\
            "Ongoing treatment 2": < list of [ ongoing treatment, planned duration , possible side effects ] >,\
            ...\
            "Ongoing treatment N": < list with ongoing treatment, planned duration and possible side effects >\
            }\
            }'
        treatment_summarizer_prompt = f'\
                            Patient information is below.\n\
                            --------------------- \n\
                            {relevant_patient_text} \n \
                            ---------------------. \n \
                            Given the patient information extract following information on their ongoing treatment only. Use only the given patient information and not prior information. \n\
                            If the information is not given in patient data specify not given. \n \
                            Provide the response in the following JSON format and do not deviate from the specified format. \n\n \
                            {response_format} \n\n \
                            Ensure to provide the response in a proper JSON format without indent with main key as {task_name} and provide it at the end of the response \n \
                            '
    return treatment_summarizer_prompt


def get_general_info_prompt(relevant_patient_text):
    # general_info_prompt = f'\
    #                 Patient information is below.\n\
    #                 --------------------- \n\
    #                 {relevant_patient_text} \n \
    #                 ---------------------. \n \
    #                 Given the patient information extract following general information. Use only the given patient information and not prior information. \n\
    #                 If the information is not given in patient data specify not given. \n \
    #                 Provide the response in the following format and do not deviate from the specified format. \n\n \
    #                 General Information: \n\n \
    #                         Patient Name: <Name of the patient>\n\
    #                         Patient DOB: <Date of Birth of the patient>\n\
    #                         Patient Phone Number: <Phone number of the patient>\n\
    #                         Patient Email: <Email of the patient>\n\
    #                         Primary Care Provider: <Name of the primary care provider>\n\
    #                         Surgeon: <Name of the surgeon>\n\
    #                         Radiation Oncologist: <Name of the radiation oncologist>\n\
    #                         Medical Oncologist: <Name of the medical oncologist>\n\
    #                         Other Providers: <Name of the other providers>\n\n\
    #                 Finally convert the above response into a proper JSON format without indent with main key as General Information and provide it at the end of the response. Make sure the json output is in the right format \n \
    #                 '
    add_str = 'Extract the following and only provide the extracted information in the output and do not have any unnecessary text in the output. \n\n'
    general_info_prompt = [f'{add_str} Patient Name',
                            f'{add_str} Patient DOB',
                            f'{add_str} Patient Phone Number',
                            f'{add_str} Patient Email',
                            f'{add_str} Primary Care Provider',
                            f'{add_str} Surgeon',
                            f'{add_str} Radiation Oncologist',
                            f'{add_str} Medical Oncologist',
                            f'{add_str} Other Providers']
    return general_info_prompt