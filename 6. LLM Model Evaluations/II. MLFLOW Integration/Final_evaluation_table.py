import pandas as pd
import glob
import re
import os.path
import datetime

# List of file names
csv_files = glob.glob("Output_CSV/*.csv")

# Define model size mappings
model_size_mapping = {
    'Bloom': '176B',
    'Bloom_internal':'176B',
    'FlanT5-XXL': '11B',
    'FlanT5-XL':'3B',
    'FlanT5': '3B',
    'Coga': '3B',
    'Flan_ul2':'20B'
}

# Create an empty DataFrame
leaderboard = pd.DataFrame(columns=['Model Name', 'Dataset', 'F1 Score', 'BERT Score', 'Blue Score', 'SentenceSim Score', 'Meteor Score', 'Rouge Score', 'SimHash Score', 'Perplexity Score', 'Bleurt Score', 'Count', 'Model Size'])

# Iterate over the scores files
for file in csv_files:
    model_name = file.split(".")[0]
    # Extract dataset and model name using regex pattern
    pattern = r'^(.*?)_(.*)$'
    match = re.match(pattern, model_name)
    if match:
        dataset = match.group(1)
        model = match.group(2)
    else:
        dataset = ""
        model = model_name
    
    # Get the model size based on the model name
    model_size = model_size_mapping.get(model, "")

    df = pd.read_csv(file)  # Assuming the scores are stored in CSV format
        # Get the file's creation date
    creation_time = os.path.getctime(file)
    creation_time = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d') 
    
    
    
    # Get the mean scores for available columns
    mean_scores = {}
    for score in leaderboard.columns[2:-2]:
        # Perform a case-insensitive match for score column names
        available_columns = [col for col in df.columns if col.lower() == score.lower()]
        if available_columns:
            if score not in ['SimHash Score', 'Perplexity Score', 'Bleurt Score']:
                mean_scores[score] = df[available_columns[0]].mean() * 100  # Multiply score by 100
            else:
                mean_scores[score] = df[available_columns[0]].mean()
        else:
            mean_scores[score] = None  # Assign null or any other desired value

    leaderboard = leaderboard.append({'Model Name': model, 'Evaluated on': dataset, **mean_scores,'Experiment Date':creation_time, 'Count': len(df), 'Model Size': model_size}, ignore_index=True)

# Move null values to the bottom of the table
leaderboard = leaderboard.sort_values(by=leaderboard.columns[2:-2].tolist(), na_position='last')

# Display the leaderboard
result = leaderboard[['Model Name', 'Evaluated on','Experiment Date', 'Count', 'Model Size', 'F1 Score', 'BERT Score', 'Blue Score', 'SentenceSim Score', 'Meteor Score', 'Rouge Score', 'SimHash Score', 'Perplexity Score', 'Bleurt Score']]


result = result[result["F1 Score"] > 4]
result = result.sort_values(["Evaluated on","Model Name"]).reset_index(drop=True)


# New table to merge
new_table = pd.DataFrame({
    'Model Name': ['Bloom', 'FlanT5-XXL', 'FlanT5-XL', 'FlanT5', 'Coga', 'Flan_ul2'],
    'Temperature': [0.3, 0.7, 0.7, 0.7, 0.7, 0.7],
    'Top P': ['-', 1, 1, 1, 1, 1],
    'Top K': ['-', 50, 50, 50, 50, 50],
    'Decoding Method': ['sample', 'Greedy', 'Greedy', 'Greedy', 'Greedy', 'Greedy'],
    'Min New Tokens': [10, 10, 10, 10, 10, 10],
    'Max New Tokens': [200, 200, 200, 200, 200, 200],
    'Stop Sequences': ['Question', '-', '-', '-', '-', '-']
})

# Merge the two tables based on the "Model Name" column
merged_table = pd.merge(result, new_table, on='Model Name', how='outer')
merged_table.to_csv("Result/SuperKnow_Model_Evaluation_table.csv", index=False)
