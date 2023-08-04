# conda create -n ak_streamlit python=3.10 anaconda
# conda activate ak_streamlit
# pip install ipykernel
# python -m ipykernel install --user --name ak_streamlit --display-name "ak_streamlit"
#pip install streamlit
# To test the streamlit installation run : streamlit hello

import streamlit as st
import pandas as pd
import numpy as np
#from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode

st.title('Superknowa Experiment Tracker')

df = pd.read_csv("./Result/leaderboard.csv")
def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

selection = dataframe_with_selections(df[['Model Name', 'InputDataset', 'Retriever', 'Reranker', 'EvaluatedOn', 'Count', 'Model Size', 'F1 Score','Meteor Score',
       'BERT Score', 'Blue Score', 'SentenceSim Score', 
       'Rouge Score', 'SimHash Score', 'Perplexity Score', 'Bleurt Score']])
#selection["x_axis"] = selection["Model Name"]+selection["InputDataset"]+selection["Retriever"]+selection["Reranker"]+selection["EvaluatedOn"]
st.write("Your selection:")
st.write(selection)

yaxis_option = st.selectbox(
    'Metric to be plotted?',
    (['F1 Score','BERT Score','Blue Score','SentenceSim Score','Meteor Score','Rouge Score','SimHash Score','Perplexity Score','Bleurt Score']))


st.bar_chart(selection, x = ["Model Name","InputDataset","Retriever","Reranker","EvaluatedOn"], y = yaxis_option)

