import requests
import json

# URL for the web service, should be similar to:
# 'http://8530a665-66f3-49c8-a953-b82a2d312917.eastus.azurecontainer.io/score'
scoring_uri = 'http://c00fb195-b93d-4f7b-9fa0-8686b91c8e82.westeurope.azurecontainer.io/score'
# If the service is authenticated, set the key or token
key = 'ZhT1II3YUp6UsrIlNFqY7WebY3XTjCkd'

# Two sets of data to score, so we get two results back
data = {"Inputs":{
	"data":[
          {"satisfaction_level": 0.57, 
          "last_evaluation": 0.98, 
          "number_project": 3, 
          "average_montly_hours": 188,
          "time_spend_company": 5, 
          "Work_accident": 0, 
          "promotion_last_5years": 0, 
          "Department": "support",
          "salary": "medium"
          }, 
          {"satisfaction_level": 0.28, 
          "last_evaluation": 0.9, 
          "number_project": 4, 
          "average_montly_hours": 275,
          "time_spend_company": 6, 
          "Work_accident": 0, 
          "promotion_last_5years": 0, 
          "Department": "marketing", 
          "salary": "low"}
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


