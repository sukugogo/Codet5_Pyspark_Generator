import streamlit as st


def fn_component_generator(model, tokenizer):
    component_prompt = ''
    with st.expander("Component Generator", expanded=True):
        tab1, tab2, tab3, tab4 = st.tabs(["Component Generator", "Delete Component", "Delete Association", "Help?"])
        with tab1:
            col1, col2 = st.columns([3, 8])
            with col1:
                current_component_id_list = set(st.session_state.component_id_list)
                etl_component_current = st.selectbox(
                    "Select Current Component",
                    current_component_id_list,
                    key='etl_component_current',
                    index=None
                )
                if etl_component_current:
                    st.session_state['current_component'] = etl_component_current

                parent_component_list = [''] + [x for x in current_component_id_list if x != etl_component_current]

                etl_component_parent = st.selectbox(
                    "Select Parent Component (if any)",
                    parent_component_list,
                    key='etl_component_parent'
                )

            with col2:
                placeholder_prompt = 'Enter Component Prompt'
                if etl_component_current:
                    if etl_component_current.startswith('INP_'):
                        placeholder_prompt = f"{placeholder_prompt}: e.g. read a json file into dataframe"
                    if etl_component_current.startswith('OUT_'):
                        placeholder_prompt = f"{placeholder_prompt}: e.g. write dataframe to a csv file"
                component_prompt = st.text_area("Component Prompt", placeholder=placeholder_prompt, height=122)

            add_association = st.button("Generate Component Association")

            if add_association:
                if etl_component_current:
                    st.session_state.assoc_component_list.append({
                        "current": etl_component_current,
                        "parent": etl_component_parent if etl_component_parent else ''
                         })
            result = {
                'current_component': etl_component_current,
                'component_prompt': component_prompt,
            }

        with tab2:
            col11, col21 = st.columns([3, 8])
            with col11:
                select_delete_component = st.selectbox(
                    "Select Component to Delete",
                    st.session_state.component_id_list,
                    key='select_delete_component'
                )
                delete_component = st.button("Delete Component")
                if delete_component:
                    st.session_state.component_id_list.remove(select_delete_component)

                    st.session_state.assoc_component_list = [
                        x for x in st.session_state.assoc_component_list
                        if select_delete_component not in [x['current'], x['parent']]
                    ]
                    st.rerun()

        with tab3:
            col12, col22 = st.columns([8, 2])
            with col12:
                st.session_state.assoc_component_list = [
                    i for n, i in enumerate(st.session_state.assoc_component_list)
                    if i not in st.session_state.assoc_component_list[:n]
                ]

                select_delete_association = st.selectbox(
                    "Select Association",
                    st.session_state.assoc_component_list,
                    key='select_delete_association'
                )
                delete_association = st.button("Delete Association")
                if delete_association:
                    st.session_state.assoc_component_list.remove(select_delete_association)
                    st.rerun()

        with tab4:
            st.write("**How to Use the Component Code Generator**")
            st.info(
                "- Select the Current component.\n"
                "   - For input components, the predict code will be converted to a dataframe.\n"
                "   - For Output components, the parent component will be written to a "
                "desired output like csv, json etc.\n"
                "   - For Adhoc/Custom components, no prompts are required."
                " The parent component dataframe will be used as the base dataframe for coluumn operations\n"
                "- Select the Parent component.\n"
                "   - If no parent is selected, the graph displays the current component as a standalone component.\n"
                "   - If parent is selected, the association is displayed in the adjacent Graph View section."
            )
            st.write("**NOTE**")
            st.info(
                "- This UI stores everything in memory since it was created for DEMO purposes.\n"
                "- Refreshing the browser will remove all the components.\n"
            )


    return result
