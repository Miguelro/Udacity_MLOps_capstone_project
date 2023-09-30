import requests
import json

# URL for the web service, should be similar to:
# 'http://8530a665-66f3-49c8-a953-b82a2d312917.eastus.azurecontainer.io/score'
scoring_uri = 'http://afcc82ca-85bd-4d21-baf4-835954f56321.westus2.azurecontainer.io/score'
# If the service is authenticated, set the key or token
key = 'gPgDZf7SzbckY8T2yk6DcCvvz5buvq0R'

# Two sets of data to score, so we get two results back
data = {"Inputs":{
	"data":[
          {
            "satisfaction_level": 0.36,
            "last_evaluation": 0.55,
            "number_project": 2,
            "average_montly_hours": 141,
            "time_spend_company": 3,
            "Work_accident": 0,
            "promotion_last_5years": 0,
            "Department": "hr",
            "salary": "medium"
          },
          {
            "satisfaction_level": 0.5,
            "last_evaluation": 0.7,
            "number_project": 3,
            "average_montly_hours": 160,
            "time_spend_company": 4,
            "Work_accident": 0,
            "promotion_last_5years": 0,
            "Department": "sales",
            "salary": "medium"
          },
      ]
    }
}
# Convert to JSON string
input_data = json.dumps(data)
with open("data.json", "w") as _f:
    _f.write(input_data)

# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Bearer {key}'

# Make the request and display the response
resp = requests.post(scoring_uri, input_data, headers=headers)
print(resp.json())


