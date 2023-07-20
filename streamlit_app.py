import streamlit as st
from steamship import Steamship


def get_param(param_name):
    query_params = st.experimental_get_query_params()
    try:
        return query_params[param_name][0]
    except:
        #st.write('Parameters is missing')
        return False
def get_params(params_names_list):
    query_params = st.experimental_get_query_params()
    responses = []
    for parameter in params_names_list:
        try:
            responses.append(query_params[parameter][0])
        except Exception as e:
            responses.append(None)
    return responses

#Pass parameters from iframe?
workspace = get_param("workspace")
package = get_param("package")
instance = get_param("instance")
token = get_param("token")

if not workspace:
    workspace="streamlit-chat-agent-213" #unique workspace name
if not package:
    package = "streamlit-chat-agent" #name of the deployed Steamship package
if not instance:
    instance = "streamlit-chat-agent-213" #unique instance name of the Steamship package
if not token:
    token = "unique-chat-id1" #JWT token

client = Steamship(workspace=workspace)
#get instance, if not found, will create one
if not st.session_state.get("instance"):
    with st.spinner("Creating chatbot..."):
        instance = client.use(package, instance)
else:
    instance = st.session_state.instance

if "token" not in st.session_state:
    st.session_state["token"] = token

if "indexed" not in st.session_state:
    with st.spinner("Loading chatbot data, this may take a few minutes.."):
        instance.invoke("initial_index")
        st.session_state["indexed"] = 1


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I'm Nurse Nina. How can I help you today?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = instance.invoke("prompt", prompt=prompt,context_id=st.session_state["token"])
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
