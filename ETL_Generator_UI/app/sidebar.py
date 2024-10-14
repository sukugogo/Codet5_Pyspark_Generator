import re
import streamlit as st


# Define function for Sidebar tasks
def etl_sidebar():

    base_components = {
        'Input_Component' : 'INP_',
        'Output_Component': 'OUT_',
        'Custom_Component': 'ADHC_'
    }

    component_id = None
    with st.sidebar:
        st.header("Pyspark ETL Code Generator")
        st.caption('---')
        component_type = st.selectbox("Select Component Type", base_components.keys(), key='component_type')
        if component_type:
            component_name = st.text_input("Component Name", max_chars=20)

        add_custom_component = st.button("Add Component")
        st.caption('---')
        st.info('NOTE:\n- The component name is prefixed and suffixed automatically  maintain uniqueness. '
                '\n- Non Alphanumeric characters are removed. \n- Spaces are replace by underscore.')
        st.caption('---')

    if add_custom_component:
        component_name = re.sub(r"\s+", '_', component_name.strip())
        component_name = re.sub(r"[^\w_:]+", '', component_name)

        component_id = base_components[component_type] + component_name
        if component_id not in st.session_state.component_id_list:
            st.session_state.component_id_list.append(component_id)

    return component_id
