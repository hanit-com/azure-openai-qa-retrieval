import os
import openai
from constants import API_KEY, RESOURCE_ENDPOINT
from llama_index import LangchainEmbedding, GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext, StorageContext
from llama_index import load_index_from_storage
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings


def setup_environment():
  os.environ["OPENAI_API_KEY"] = API_KEY
  os.environ["OPENAI_API_BASE"] = RESOURCE_ENDPOINT

  openai.api_type = "azure"
  openai.api_version = "2022-12-01"
  openai.api_base = os.getenv('OPENAI_API_BASE')
  openai.api_key = os.getenv("OPENAI_API_KEY")


def get_service_context():
  deployment_name = "text-davinci-003"

  llm = AzureOpenAI(deployment_name=deployment_name, temperature=1.0)
  llm_predictor = LLMPredictor(llm=llm)
  embedding_llm = LangchainEmbedding(OpenAIEmbeddings(), embed_batch_size=1)

  max_input_size = 3000
  num_output = 256
  chunk_size_limit = 1000
  max_chunk_overlap = 20
  prompt_helper = PromptHelper(max_input_size=max_input_size, num_output=num_output, max_chunk_overlap=max_chunk_overlap, chunk_size_limit=chunk_size_limit)
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper, embed_model=embedding_llm)
  
  return service_context


def get_index():
  service_context = get_service_context()
  data_path = "context_data/data"
  storage_path = "./storage"

  is_local_vector_store = os.path.exists(storage_path) and os.listdir(storage_path)

  if is_local_vector_store:
    print("loading index from storage")
    storage_context = StorageContext.from_defaults(persist_dir=storage_path)
    index = load_index_from_storage(storage_context, service_context=service_context)
  else:
    print("creating new index...")
    documents = SimpleDirectoryReader(data_path).load_data()
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
    index.storage_context.persist()
    print("index created")

  return index


def askGPT(index):

  template = "Shortly answer the following question, do not elaborate. {}"
  query_engine = index.as_query_engine()

  while True:
      prompt = input("Prompt: ")

      if prompt == "exit":
        break

      query = template.format(prompt)
      response = query_engine.query(query)
      
      print(f"Completion: {response.response}")


"""
Questions

What was the venue of the coronation?
Were tiaras allowed at the ceremony?
What transportation did Charles and Camilla use to get to the abbey?
Did the Prince of Wales participate in the service?

"""

setup_environment()
index = get_index()
askGPT(index)