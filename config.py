import os
from dotenv import load_dotenv

load_dotenv()

# TeamCity Configuration
TEAMCITY_URL = os.getenv("TEAMCITY_URL", "https://your-teamcity-instance.com")
TEAMCITY_API_KEY = os.getenv("TEAMCITY_API_KEY", "your-teamcity-api-key")
BUILD_TYPE_ID = os.getenv("BUILD_TYPE_ID", "your-build-type-id")

# Jira Configuration
JIRA_URL = os.getenv("JIRA_URL", "https://your-jira-instance.atlassian.net")
JIRA_API_KEY = os.getenv("JIRA_API_KEY", "your-jira-api-key")
JIRA_USER_EMAIL = os.getenv("JIRA_USER_EMAIL", "your-email@example.com")


# Google Sheets Configuration
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "your-google-sheet-id")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "your-sheet-name")
# Base64 encoded service account JSON
GOOGLE_SERVICE_ACCOUNT_B64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_B64", "your-base64-encoded-json")


# --- Column Mapping ---
# Maps Jira issue fields to Google Sheet column headers.
# This allows for easy adjustments without changing the core logic.
# Format: "Jira Field Name": "Google Sheet Column Name"
JIRA_TO_SHEET_COLUMN_MAPPING = {
    "key": "JIRA_KEY",
    "fields.summary": "SUMMARY",
    "fields.customfield_11111": "MANUFACTURER",
    "fields.customfield_11110": "SHELF_TYPE",
    "fields.parent.fields.summary": "Parent Name",
    "build_date": "DEPLOY_DATE",

    # Add more fields as needed. You can use dot notation for nested fields.
    # "fields.issuetype.name": "Issue Type",
    # "fields.assignee.displayName": "Assignee"
    # "fields.priority.name": "Priority",
    # "fields.status.name": "Status",
    # "fields.reporter.displayName": "Reporter",
}
