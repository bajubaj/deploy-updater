import base64
import json
import gspread
from google.oauth2.service_account import Credentials
import config
import os
import sys

def get_google_sheets_client(service_account_path):
    """Authenticates with Google Sheets and returns a client."""
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file(service_account_path, scopes=scopes)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        print(f"Error: `{service_account_path}` not found.")
        print("Please make sure the service account file is in the same directory as the application.")
        raise
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        raise

def get_last_processed_deployment_id(sheet):
    """Retrieves the last processed deployment ID from cell A1."""
    try:
        return sheet.acell('A1').value
    except gspread.exceptions.CellNotFound:
        return None
    except Exception as e:
        print(f"Error reading last processed deployment ID: {e}")
        return None

def update_google_sheet(sheet, data):
    """
    Appends new rows to the Google Sheet with Jira ticket information,
    matching the column order of the existing header.
    
    Args:
        sheet: The gspread worksheet object.
        data (list of dicts): A list of dictionaries, where each dictionary
                               represents a Jira ticket.
    """
    if not data:
        print("No new data to update in Google Sheet.")
        return

    try:
        # Read the header row from the sheet to get the exact column order.
        header = sheet.row_values(1)
        if not header:
            print("Error: Could not find header row in Google Sheet. Cannot proceed.")
            return

        # Create a reverse mapping from sheet column name to Jira field key.
        # e.g., {"Jira Key": "key", "Summary": "fields.summary"}
        sheet_to_jira_mapping = {v: k for k, v in config.JIRA_TO_SHEET_COLUMN_MAPPING.items()}
        
        rows_to_append = []
        for item in data:
            # Build the row in the correct order by iterating through the sheet's header.
            row = []
            for column_name in header:
                # Find the Jira key for the current column.
                jira_field_key = sheet_to_jira_mapping.get(column_name)
                
                # Get the value from the Jira item data.
                if jira_field_key:
                    value = get_nested_value(item, jira_field_key)
                    row.append(value if value is not None else "")
                else:
                    # If a column from the sheet is not in our mapping, append an empty string.
                    row.append("")
            
            rows_to_append.append(row)
            
        sheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
        print(f"Successfully appended {len(rows_to_append)} rows to the sheet.")

    except Exception as e:
        print(f"Error updating Google Sheet: {e}")
        raise

def update_last_processed_deployment_id(sheet, deployment_id):
    """Updates cell A1 with the latest deployment ID."""
    try:
        # Pass a list of lists to update a single cell
        sheet.update('A1', [[deployment_id]])
        print(f"Successfully updated last processed deployment ID to: {deployment_id}")
    except Exception as e:
        print(f"Error updating last processed deployment ID: {e}")
        raise

def get_nested_value(data_dict, key):
    """
    Safely retrieves a nested value from a dictionary using dot notation.
    Handles special cases like checkbox fields which are lists of objects.
    Example: get_nested_value(issue, "fields.summary")
    """
    keys = key.split('.')
    value = data_dict
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value.get(k)
        else:
            return None
    
    # If the final value is a list of dicts (like a checkbox field), format it.
    if isinstance(value, list) and all(isinstance(i, dict) and 'value' in i for i in value):
        return ', '.join(item['value'] for item in value)

    return value
