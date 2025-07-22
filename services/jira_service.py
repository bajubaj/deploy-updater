import requests
from requests.auth import HTTPBasicAuth
import config

def get_jira_issue_details(issue_key):
    """
    Fetches details for a specific Jira issue.
    """
    url = f"{config.JIRA_URL}/rest/api/3/issue/{issue_key}"
    
    auth = HTTPBasicAuth(config.JIRA_USER_EMAIL, config.JIRA_API_KEY)
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Jira issue not found: {issue_key}")
        else:
            print(f"Error fetching Jira issue {issue_key}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Jira issue {issue_key}: {e}")
        return None
