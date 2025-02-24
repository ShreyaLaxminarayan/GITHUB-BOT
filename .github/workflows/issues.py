import os
import requests
from datetime import datetime

repo_owner = "dotnet"  
repo_name = "runtime"    
bot_username = "@GITHUB_BOT"     

issues_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"


github_token = secrets.PAT_TOKEN
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}

def check_mentions():
    response = requests.get(issues_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching issues: {response.status_code}")
        return

    issues = response.json()
    
    for issue in issues:
        if "pull_request" in issue and issue["state"] == "open":
            if f"@{bot_username}" in issue["body"]:
                print(f"Found mention in issue #{issue['number']}: {issue['title']}")
                # Trigger CI job here if needed
                # For example, you could create a comment in the issue:
                comment_url = issue["comments_url"]
                comment_payload = {
                    "body": f"@{bot_username} was mentioned, CI process triggered."
                }
                comment_response = requests.post(
                    comment_url, headers=headers, json=comment_payload
                )
                if comment_response.status_code == 201:
                    print(f"Comment added to issue #{issue['number']}")
                else:
                    print(f"Failed to add comment to issue #{issue['number']}")
            else:
                print(f"No mention found in issue #{issue['number']}.")

if __name__ == "__main__":
    check_mentions()

