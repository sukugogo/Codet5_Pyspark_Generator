import os
import time
import torch
import streamlit as st
from transformers import RobertaTokenizer, T5ForConditionalGeneration
from accelerate import Accelerator


@st.cache_resource
def fn_preload_model():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"  # Set the desired GPU IDs

    my_bar = st.progress(0, text='Loading the pretrained model ...')
    for percent_complete in range(101):
        # Initialize the accelerator
        #accelerator = Accelerator()

        model_name = "Salesforce/codet5-small"
        model_save_file = 'app/data/Final_Model_State.pt'

        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        model.load_state_dict(torch.load(model_save_file, map_location=torch.device('cpu')))

        model.eval()
        my_bar.progress(percent_complete)
    my_bar.empty()
    return model, tokenizer


def fn_predict_from_prompt(text_prompt, model, tokenizer):

    inputs = tokenizer('Translate prompt to PySpark: ' + text_prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=150)
    predicted_text = tokenizer.decode(outputs[0])

    predicted_text = predicted_text.replace(tokenizer.pad_token, '').replace('<s>', '').replace('</s>', '')

    return predicted_text
