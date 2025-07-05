#step 1: setup ui with streamlit(model provider, model, prompt, web_search, query)
import streamlit as st
st.set_page_config(page_title = "LangGraph agent ui", layout = "wide")
st.title("AI Chatbot Agents")
st.write("Create and Interact with AI Agents!")
prompt = st.text_area("define your ai agent:", height = 70, placeholder = "Type your system promopt here ...")
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]    

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq model", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model= st.selectbox("select OpenAI model", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow web search")
user_query = prompt = st.text_area("Enter your query:", height = 150, placeholder = "Ask Anything")

API_URL = "https://aiagentbasicdemo-production.up.railway.app/chat"
if st.button("Ask Agent!"):
    if user_query.strip():
      #step 2: connect wiht backend via url
      import requests
      payload = {
          "model_name": selected_model,
          "model_provider": provider,
          "prompt": prompt,
          "messages": [user_query],
          "allow_search": allow_web_search
      }
      response = requests.post(API_URL,json=payload)
      if response.status_code == 200:
        response_data= response.json()
        if "error" in response_data:
           st.error(response_data["error"])
        else:
           st.subheader("Agent Response")
           st.markdown(f"**Final Response: **{response_data}")

