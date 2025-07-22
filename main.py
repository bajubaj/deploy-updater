from services import google_sheets_service, teamcity_service, jira_service
import config
import os
import sys

def main():
    """Main function to orchestrate the update process."""
    
    print("Starting Jira update process...")
    
    # --- Path handling for PyInstaller ---
    # Determine the base path, which works for both development and a frozen .exe
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS'.
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    service_account_path = os.path.join(base_path, 'service_account.json')
    # --- End Path handling ---

    # 1. Initialize Google Sheets client and get the worksheet
    try:
        g_client = google_sheets_service.get_google_sheets_client(service_account_path)
        sheet = g_client.open_by_key(config.GOOGLE_SHEET_ID).worksheet(config.GOOGLE_SHEET_NAME)
    except Exception as e:
        print(f"Failed to open Google Sheet. Aborting. Error: {e}")
        return

    # 2. Get the last processed deployment ID
    last_deployment_id = google_sheets_service.get_last_processed_deployment_id(sheet)
    print(f"Last processed deployment ID: {last_deployment_id}")

    # 3. Fetch new deployments from TeamCity
    deployments = teamcity_service.get_deployments(since_deployment_id=last_deployment_id)
    if not deployments:
        print("No new deployments found.")
        return

    print(f"Found {len(deployments)} new deployments.")

    all_jira_issues_data = []
    latest_deployment_id = None

    # 4. For each new deployment, extract Jira keys
    for i, deployment in enumerate(sorted(deployments, key=lambda d: d['id']), 1):
        deployment_id = deployment['id']
        print(f"Processing deployment {i}/{len(deployments)}: ID {deployment_id}")

        # Get build details for date and tags
        build_details = teamcity_service.get_build_details(deployment_id)
        build_date = build_details.get('finishDate', '')
        release_tag = ', '.join([tag['name'] for tag in build_details.get('tags', {}).get('tag', [])])

        commit_messages = teamcity_service.get_commit_messages_from_build(deployment_id)
        
        deployment_jira_keys = set()
        for msg in commit_messages:
            jira_keys = teamcity_service.extract_jira_keys_from_commit(msg)
            deployment_jira_keys.update(key.upper() for key in jira_keys)

        if not deployment_jira_keys:
            print(f"  No Jira keys found in deployment {deployment_id}.")
            continue

        print(f"  Found {len(deployment_jira_keys)} unique Jira keys: {deployment_jira_keys}")

        # 5. Fetch details for each unique Jira key in this deployment
        for key in deployment_jira_keys:
            issue_details = jira_service.get_jira_issue_details(key)
            if issue_details:
                # Add deployment-specific info to the issue data
                issue_details['build_date'] = build_date
                issue_details['release_tag'] = release_tag
                all_jira_issues_data.append(issue_details)
        
        # Keep track of the latest deployment ID processed in this run
        if i == len(deployments):
            latest_deployment_id = deployment_id

    # 6. Update the Google Sheet with all the new data from all deployments
    if all_jira_issues_data:
        google_sheets_service.update_google_sheet(sheet, all_jira_issues_data)
    else:
        print("No Jira issue details to update in the sheet.")
        
    # 7. Update the last processed deployment ID in the sheet
    if latest_deployment_id:
        google_sheets_service.update_last_processed_deployment_id(sheet, latest_deployment_id)

    print("Jira update process finished successfully.")

if __name__ == "__main__":
    main()
