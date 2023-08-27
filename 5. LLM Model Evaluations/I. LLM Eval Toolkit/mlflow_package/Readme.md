## MLFLOW Package 


## Step 1

### Install dependencies
Run `python3 setup.py install` 

## Step 2

### Import the library
`import mlflow_utils`

## Step 3

### Set the path of your evaluation directory

```
path="set the path of your evalution result DIR"
mlflow_utils.run_mlflow(path)
```

## Step 4
### Start the MLFLow dashboards locally

`mlflow ui`

check the leaderboard: 

[http://127.0.0.1:5000](http://127.0.0.1:5000)



