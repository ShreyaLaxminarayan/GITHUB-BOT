import os
import requests
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_PAT_TOKEN")
username = "your-username"  

# Authenticate to GitHub API using the token
g = Github(GITHUB_TOKEN)

# Get notifications where the user is mentioned
notifications = g.get_user().get_notifications()

for notification in notifications:
    # Check if the notification is a pull request and your username is mentioned
    if 'pull_request' in notification.subject.url:
        pr_url = notification.subject.url
        pr = g.get_repo(notification.repository.full_name).get_pull(pr_url.split('/')[-1])
        
        # Check if your username is mentioned in the PR's body or comments
        if username in pr.body or any(username in comment.body for comment in pr.get_comments()):
            print(f"PR {pr.title} has mentioned you. Merging...")
            
            # Merge the PR
            pr.merge()
            print(f"Successfully merged PR {pr.title}")
        else:
            print(f"PR {pr.title} has not mentioned you.")
