import requests
import json

# URL for the web service, should be similar to:
# 'http://bfd454ae-2063-4b1b-a45b-82f097e5a0e7.southcentralus.azurecontainer.io/score'
scoring_uri = 'http://bfd454ae-2063-4b1b-a45b-82f097e5a0e7.southcentralus.azurecontainer.io/score'
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


