# Azure OpenAI Embedding

This repository utilizes Azure OpenAI Embedding service to answer questions and interact with your own documented data. 

## Prerequisites
You should have an Azure account and a running instance of OpenAI.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/your-project.git
   ```

2. Create a Python environment:

   ```shell
   python -m venv .env
   ```

3. Activate the environment:

   ```shell
   source .env/bin/activate
   ```

4. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Configuration

1. Inside 'constants.py', complete the API key and the Azure resource endpoint base.  
Select an instance on the [Cognitive Services Hub](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/OpenAI) and go to "Keys and Endpoints".  
Use either "KEY 1" or "KEY 2" and the "Endpoint" field.

   ```python
   API_KEY = ""
   RESOURCE_ENDPOINT = ""
   ```
2. Add your data files to the 'context_data/data' directory.


## Usage

Run:

```shell
python azure_openai.py
```

Prompt example:  
(Using data from the Wikipedia page [Coronation of Charles III and Camilla](https://en.wikipedia.org/wiki/Coronation_of_Charles_III_and_Camilla)).
```shell
Prompt: Where tiaras allowed at the ceremony?
Completion: 
No, tiaras were not allowed at the ceremony.
Prompt: What was the venue for the coronation?
Completion: 
The venue for the coronation was Westminster Abbey.
```

