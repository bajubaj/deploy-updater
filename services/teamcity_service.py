import requests
import re
import config

def get_deployments(since_deployment_id=None):
    """
    Fetches all successful deployments since a specific deployment ID.
    If since_deployment_id is None, it fetches the latest successful deployment.
    """
    headers = {
        "Authorization": f"Bearer {config.TEAMCITY_API_KEY}",
        "Accept": "application/json"
    }
    
    # This locator finds all successful builds for the specified build type.
    # You might need to adjust this based on your TeamCity setup.
    locator = f"buildType:{config.BUILD_TYPE_ID},status:SUCCESS,state:finished"
    
    if since_deployment_id:
        # This will fetch builds since the last processed one.
        # Note: TeamCity's API might require a build number or other locator.
        # This is a conceptual example. You might need to adjust the query.
        locator += f",sinceBuild:(id:{since_deployment_id})"

    url = f"{config.TEAMCITY_URL}/app/rest/builds/?locator={locator}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        builds = response.json().get("build", [])
        
        # If we only need the latest build when no since_id is provided
        if not since_deployment_id and builds:
            return [builds[0]]
            
        return builds

    except requests.exceptions.RequestException as e:
        print(f"Error fetching deployments from TeamCity: {e}")
        return []

def get_commit_messages_from_build(build_id):
    """
    Fetches all commit messages associated with a specific TeamCity build.
    """
    headers = {
        "Authorization": f"Bearer {config.TEAMCITY_API_KEY}",
        "Accept": "application/json"
    }
    # Add fields=change(comment) to fetch the commit message in the same request
    url = f"{config.TEAMCITY_URL}/app/rest/changes?locator=build:(id:{build_id})&fields=change(comment)"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        changes = response.json().get("change", [])
        return [change.get("comment", "") for change in changes]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching commit messages from TeamCity for build {build_id}: {e}")
        return []

def extract_jira_keys_from_commit(commit_message):
    """
    Extracts Jira keys (e.g., 'PROJ-123') from a commit message using regex.
    """
    # This regex looks for patterns like 'PROJ-123' or 'story/PROJ-1234'
    jira_key_pattern = r'([A-Z]{2,}-\d+)'
    return re.findall(jira_key_pattern, commit_message, re.IGNORECASE)

def get_build_details(build_id):
    """
    Fetches detailed information for a specific TeamCity build, including tags and date.
    """
    headers = {
        "Authorization": f"Bearer {config.TEAMCITY_API_KEY}",
        "Accept": "application/json"
    }
    # Fetching build details, including tags
    url = f"{config.TEAMCITY_URL}/app/rest/builds/id:{build_id}?fields=finishDate,tags"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching build details from TeamCity for build {build_id}: {e}")
        return None
