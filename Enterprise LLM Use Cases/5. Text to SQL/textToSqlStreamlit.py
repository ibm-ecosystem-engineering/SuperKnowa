#!pip install pydantic==1.10.9
import pandas as pd
import sqlite3
from db_connectors import SQLiteConnector
from prompt_formatters import RajkumarFormatter
from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline
import streamlit as st

def llm_response(prompt):
    tokenizer = AutoTokenizer.from_pretrained("NumbersStation/nsql-6B")
    model = AutoModelForCausalLM.from_pretrained("NumbersStation/nsql-6B")
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=1000)
    response = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return   response[len(prompt):]


def get_sql(instruction: str, max_tokens: int = 300) -> str:
    prompt = formatter.format_prompt(instruction)
    res = llm_response(prompt)
    return formatter.format_model_output(res)

queries = [         # illogical question
    "How many rows are in the loan database?",                              # basic 
    "What is the breakdown of the grade column?",                           # basic
    "Count the number of rows where the loan status is any of the following ['Charged Off', 'Default', 'Does not meet the credit policy. Status:Charged Off', 'In Grace Period', 'Late (31-120 days)', 'Late (16-30 days)']"]

df = pd.read_csv('loan.csv')
# conn = sqlite3.connect('loan.db')
# df.to_sql('loan', conn, index=False)

DATABASE = "loan.db"
TABLES = []  # list of tables to load or [] to load all tables

# Get the connector and formatter
sqlite_connector = SQLiteConnector(
    database_path=DATABASE
)
sqlite_connector.connect()
if len(TABLES) <= 0:
    TABLES.extend(sqlite_connector.get_tables())

print(f"Loading tables: {TABLES}")
db_schema = [sqlite_connector.get_schema(table) for table in TABLES]
formatter = RajkumarFormatter(db_schema)




######STREAMLIT##########
st.header("Text To SQL")
st.subheader("Source Table")
st.dataframe(df.head())

query = st.text_input('Text Query',queries[0])

sql = get_sql(query)
res = sql

st.subheader("SQL Query Generated Using LLM")
st.write(res)

df_res = sqlite_connector.run_sql_as_df(sql)


st.subheader("Result of runnning the SQL query on table")
st.dataframe(df_res)