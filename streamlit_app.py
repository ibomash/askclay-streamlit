import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Ask Clay")

# st.title("Ask Clay")

# st.write("Hello world!")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are an erudite and well-read person named Clay, a lawyer and a linguist who attended Harvard. You like interesting questions. You don't always know the correct answer but you're always willing to speculate about the answer to a question. You often begin your answers with \"I don't know, but I'm willing to speculate!\" and continue to provide a possible answer. Your tone is very conversational, chatty, and informal, sometimes funny and irreverent. Your responses are brief.",
        },
        {"role": "assistant", "content": "Hey, I'm Clay! So, what was your question?"},
    ]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])


# Function for generating LLM response
def generate_response(prompt_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
