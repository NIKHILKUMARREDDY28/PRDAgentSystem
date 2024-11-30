# To install required packages:
# pip install crewai==0.22.5 streamlit==1.32.2

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import streamlit as st

from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional




class MyCustomHandler(BaseCallbackHandler):

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name).write(outputs['output'])
