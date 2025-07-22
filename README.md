# Jira Updater

This project automates the process of updating a Google Sheet with Jira ticket information after a TeamCity deployment.

## Setup

### 1. Prerequisites

- Python 3.x
- `python3-venv` package. If you don't have it, you can install it on Debian/Ubuntu with:
  ```bash
  sudo apt-get install python3-venv
  ```

### 2. Create and Activate Virtual Environment

First, create a virtual environment to isolate the project's dependencies:

```bash
python3 -m venv .venv
```

Next, activate the virtual environment:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root of the project directory. This file will store your sensitive credentials.

```
TEAMCITY_URL="https://your-teamcity-instance.com"
TEAMCITY_API_KEY="your-teamcity-api-key"
BUILD_TYPE_ID="your-build-type-id"

JIRA_URL="https://your-jira-instance.atlassian.net"
JIRA_API_KEY="your-jira-api-key"
JIRA_USER_EMAIL="your-email@example.com"

GOOGLE_SHEET_ID="your-google-sheet-id"
GOOGLE_SHEET_NAME="your-sheet-name"
GOOGLE_SERVICE_ACCOUNT_B64="your-base64-encoded-json"
```

**Note:** Remember to add `.env` to your `.gitignore` file to prevent committing it to version control.

## How to Run

To run the script and update your Google Sheet, execute the following command from the project's root directory:

```bash
python -m jira_updater.main
``` 

NOTE: Make sure VPN is enabled.
