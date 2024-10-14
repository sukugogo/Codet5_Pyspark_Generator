import json
import graphviz
import streamlit as st


BOILER_PLATE_first = """
from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder.appName("PysparkCodeGen_DEMO").getOrCreate()
"""

BOILER_PLATE_last = """
# Stop the Spark session
spark.stop()
"""


def fn_code_view(model, tokenizer):
    with st.expander("Results View", expanded=True):
        tab1, tab2, tab3, tab4 = st.tabs(["Graph View", "Code View", "Model Info", "Help?"])

        with tab1:
            association_list = []
            components_already_associated = []
            all_components = list(set(st.session_state.component_id_list))
            graph_string = ''

            for item in all_components:
                comp_shape = 'cylinder' if item.startswith('INP_') or item.startswith('OUT_') else 'component'
                graph_string = graph_string + f"{item} [shape={comp_shape}, color=grey] \n"

            for dictionary in st.session_state.assoc_component_list:
                if dictionary not in association_list:
                    association_list.append(dictionary)

            for item in association_list:
                if item['parent'] != '':
                    graph_string = graph_string + f"{item['parent']} -> {item['current']} \n"
                    components_already_associated.append(item['current'])
                    components_already_associated.append(item['parent'])

            for item in all_components:
                if item not in components_already_associated:
                    graph_string = graph_string + f"{item} \n"

            # Display the chart
            graph = f"""
                digraph {{
                  {graph_string}
                }}
                """
            st.graphviz_chart(graph)

        with tab2:
            st.code(BOILER_PLATE_first, language="python")

            all_predictions = ''
            for key, value in st.session_state.prediction_list.items():
                column_name_dict = value['column_dict']
                column_prompt_dict = value['result_dict']
                all_predictions = all_predictions + f"# ----- COMPONENT: {key} ----- \n"
                for idx in range(10):
                    col_name = column_name_dict.get(f'COL_{idx}')
                    prompt = column_prompt_dict.get(f'PROMPT_{idx}')
                    prediction = column_prompt_dict.get(f'PREDICTED_{idx}', '')
                    if col_name and prompt:
                        prediction = ''.join(prediction.split('=')[1:]) if '=' in prediction else prediction
                        all_predictions = all_predictions + f"#{col_name}: \n" + f"{key}['{col_name}'] =" + prediction + "\n"

                st.code(all_predictions, language="python")
                if len(column_name_dict) > 0 and len(column_prompt_dict) > 0:
                    st.code(BOILER_PLATE_last, language="python")
        with tab3:
            # Print model details
            st.write(f"**Model Information**")
            st.code(f"- Model Name: CodeT5-base \n"
                    f"- Architecture: {model.config.architectures[0]} \n"
                    f"- Number of Parameters: {model.num_parameters():,} \n"
                    f"- Vocabulary Size: {len(tokenizer)} \n")
            st.write(f"**Model Config**")
            st.code(json.dumps(model.config.to_dict(), indent=4))
        with tab4:
            st.write(f"**Session State**")
            st.code(
                f"current_component: {st.session_state.current_component}\n"
                f"component_id_list: {st.session_state.component_id_list}\n"
                f"assoc_component_list: {st.session_state.assoc_component_list}\n"
                f"prediction_list: {st.session_state.prediction_list}\n"
            )

            st.write(f"**Helpful**")
            st.code(
                f"column_name_dict: {column_name_dict}\n"
                f"column_prompt_dict: {column_prompt_dict}\n"
                f"all_components: {all_components}\n"
                f"components_already_associated: {components_already_associated}\n"
            )
            #st.write(f"column_prompt_dict: {column_prompt_dict}")
    return 1
