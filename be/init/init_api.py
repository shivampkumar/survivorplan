import os
import openai
import os
import random
import numpy as np
import torch

def init_api(api_key, azure_endpoint, api_version):
    '''
    Initialize the AzureOpenAI API and set the environment variables
    '''

    os.environ["TOKENIZERS_PARALLELISM"]='false' 
    os.environ["OPENAI_API_KEY"] =  api_key
    os.environ["AZURE_OPENAI_API_KEY"] =  api_key
    os.environ["OPENAI_API_BASE"] = azure_endpoint
    os.environ["OPENAI_API_VERSION"] = api_version
    os.environ["OPENAI_API_TYPE"] = "azure"


    openai.api_type = "azure"
    openai.api_base = azure_endpoint
    openai.api_version = api_version
    openai.api_key = api_key
    openai.end_point = azure_endpoint



def seed_everything(seed=0):
    # To fix the random seed
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # backends
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False