"""Streamlit app for interacting with an LLM.

This app allows users to input messages and receive responses from a language model chain.
The responses are streamed in real-time to the display.
"""

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from chat.chain_setup import ChatAssistant


def main():
    """Main function to run the Streamlit app."""
    st.title("LLM Chain Invocation App")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)

    # Input for user messages and handle response streaming
    user_input = st.chat_input("Your message:")
    if user_input is not None and user_input != "":
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        with st.chat_message("Human"):
            st.markdown(user_input)

        with st.chat_message("AI"):
            stream = ChatAssistant().chain.stream(
                {"input": user_input}, {"configurable": {"session_id": "unused"}}
            )
            response = st.write_stream(stream)

        st.session_state.chat_history.append(AIMessage(content=response))


if __name__ == "__main__":
    main()
