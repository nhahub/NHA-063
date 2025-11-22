from Agents.state import State
from huggingface_hub import InferenceClient
import re, json
from tavily import TavilyClient
from Agents.Rag import Rag
import streamlit as st
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

Hf_token = st.secrets["HF_token"]
travily_token = st.secrets["Travily_token"]
gemini_key = st.secrets["Gemini_key"]



@tool
def get_grammar_correction(statment: str) -> str:
    # TODO add the FT model later 
    """
    Corrects the grammar of the user's sentence.

    Input:
        statement (str): A raw user sentence that may contain grammatical errors.

    Output:
        str: The corrected version of the sentence with proper grammar.
        
    Usage:
        The LLM should call this tool when it detects the user’s input
        contains grammar mistakes or could be phrased more naturally.
        The tool returns ONLY the corrected sentence with no extra text.
    """
    print('\n==========================grammer check tool \n')
    return "corrected grammer sentance"

tools = [get_grammar_correction]
llm = init_chat_model("google_genai:gemini-2.0-flash", api_key = gemini_key)
llm_with_tools = llm.bind_tools(tools, enforce_tool_use=False)


grammer_explain = Rag()
client = InferenceClient(
    api_key=Hf_token,
)

# call the model
def call_model(prompt, model_name = "HuggingFaceTB/SmolLM3-3B",  temperature=0.5, top_p = 0.5, stream = False): 
    completion = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature= temperature,
    top_p= top_p,
    stream=stream, # send wonce finished
    )
    raw_output = completion.choices[0].message.content
    if "<think>" in raw_output:
        return re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL).strip()
    return raw_output



# language classifier and intent: 
def classify_input(state:State) -> State:

    prompt = f"""
    You are a text classifier for a chatbot that helps users practice English.

    Classify the user's input as:
    - language: "english" or "arabic"
    - intent: one of ["chat", "grammar_question", "fact_question"]
    GENERATE ONLY ONE RESPONCE

    Respond in JSON ONLY:
    {{"language": "...", "intent": "..."}}.

    User input: "{state['user_input']}"
    """
    res = call_model(prompt=prompt, model_name="HuggingFaceTB/SmolLM3-3B")

    try:
        res = json.loads(call_model(prompt=prompt, model_name="HuggingFaceTB/SmolLM3-3B"))
        state["intent"], state["language"] = res["intent"], res["language"]
        if state["language"] == "arabic" : state['status_message'] = "🌐 Translator agent working..."
        
    except : 
        print("error ecured")
    
    return state


# translator agent :
def translator(state : State) -> State: 
    client = InferenceClient(
        provider="hf-inference",
        api_key=Hf_token,
    )

    result = client.translation(
    state['user_input'],
    model="Helsinki-NLP/opus-mt-ar-en",
    )
    state['translated_input'] = result.translation_text
    state["status_message"] = "🔍 Classifying your input..."

    return state


# fact search
def fact_search(state: State) -> State: 
    tavily_client = TavilyClient(api_key=travily_token)
    query = state['user_input'] if state['language'] == 'english' else state['translated_input']
    response = tavily_client.search(query=query,
                                    max_results = 1)["results"][0]
    content, url  = response["content"], response["url"] 
    state['fact_answer'] = f"""
        \n{content}\nFor more info visit {url}
    """
    
    return state

# grammar_explanation
def grammar_explanation_Rag(state: State) -> State: 
    query = state['user_input'] if state['language'] == 'english' else state['translated_input']
    state['grammar_explanation'] = grammer_explain.explain(query)
    return state
 



def chat(state: State)-> State:
    query = state['user_input'] if state['language'] == 'english' else state['translated_input']
    state['messages'].append({"role": "user","content": query})
    state['messages'] = [llm_with_tools.invoke(state["messages"])]
    state['chat_response'] = state["messages"][-1].content
    return state
    
# final composer # TODO lem l denya b2a w mmken guardrail 
def final_composer(state: State) -> State: 
    state['final_output'] = (
    state.get("grammar_explanation")
    or state.get("fact_answer")
    or state.get("chat_response")
    )
    state['status_message'] = "✨ Final response ready."
    return state
