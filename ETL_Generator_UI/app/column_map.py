import streamlit as st
from model_predictions import fn_predict_from_prompt


def fn_column_map(model, tokenizer):
    component_prompt = ''
    with st.expander("Column Mapper", expanded=True):
        tab1, tab2 = st.tabs(["Column Generator", "Help?"])
        etl_component_current = st.session_state.current_component
        with tab1:
            col1, col2 = st.columns([3, 8])
            with col1:
                column_name_dict = {}
                column_prompt_dict = {}
                for idx1 in range(5):
                    column_name_dict[f'COL_{idx1}'] = st.text_input(
                        f"[{idx1}] Enter Column Name",
                        key=f'C0L_{idx1}'
                    )
            with col2:
                for idx2 in range(5):
                    column_prompt_dict[f'PROMPT_{idx2}'] = st.text_input(
                        f"[{idx2}] Enter Column Prompt for Mapping Rule",
                        key=f'PROMPT_{idx2}'
                    )

                    if column_prompt_dict.get(f'PROMPT_{idx2}', ''):
                        text_prompt = column_prompt_dict[f'PROMPT_{idx2}']
                        column_prompt_dict[f'PREDICTED_{idx2}'] = fn_predict_from_prompt(text_prompt, model, tokenizer)
        with tab2:
            st.write("**How to Use the Column Code Generator**")
            st.info(
                "- Generate column level mappings for the component selected in the Component Generator section.\n"
                "- Provide a Column Name and corresponding prompt to generate the mapping rule.\n"
            )

            st.write("**NOTE**")
            st.info(
                "- This UI stores everything in memory since it was created for DEMO purposes.\n"
                "- Refreshing the browser will remove all the column mappings.\n"
                "- The number of columns is limited to 5 per component.\n"
            )

    res_column_name_dict = {k: v for k, v in column_name_dict.items() if v}
    res_column_prompt_dict = {k: v for k, v in column_prompt_dict.items() if v}

    st.session_state.prediction_list[etl_component_current] = {
        'column_dict': res_column_name_dict,
        'result_dict': res_column_prompt_dict
    }
