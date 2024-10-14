import torch
import streamlit as st
from sidebar import etl_sidebar
from code_view import fn_code_view
from column_map import fn_column_map
from component import fn_component_generator
from model_predictions import fn_preload_model


if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Pyspark Generator")

    # Initialize session state variables if not present
    st.session_state['current_component'] = ''
    st.session_state['prediction_list'] = {}
    for val in ['component_id_list', 'assoc_component_list']:
        if val not in st.session_state:
            st.session_state[val] = []

    model, tokenizer = fn_preload_model()

    component_id = etl_sidebar()

    col1, col2 = st.columns([8, 6])
    with col1:
        current_component_dict = fn_component_generator(model, tokenizer)
        if len(current_component_dict) > 0:
            fn_column_map(model, tokenizer)
    with col2:
        fn_code_view(model, tokenizer)
        #st.write(column_dict1)
        #st.write(column_dict2)











