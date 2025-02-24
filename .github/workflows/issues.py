import requests
import os

API_URL = "https://api.github.com"
GITHUB_TOKEN = secrets.PAT_TOKEN
REPO = "dotnet/runtime"  
BOT_MENTION = "@ShreyaLaxminarayan/GITHUB_BOT"  
  
def get_comments_for_pr(pr_number):
    url = f"{API_URL}/repos/{REPO}/issues/{pr_number}/comments"
    response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
    response.raise_for_status()
    return response.json()

def get_open_prs():
    url = f"{API_URL}/repos/{REPO}/pulls"
    response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
    response.raise_for_status()
    return response.json()

def check_mentions_in_comments():
    prs = get_open_prs()
    
    for pr in prs:
        pr_number = pr['number']
        comments = get_comments_for_pr(pr_number)
        
        for comment in comments:
            if BOT_MENTION in comment['body']:
                print(f"Bot mentioned in PR #{pr_number} by {comment['user']['login']}")
                reply_to_comment(pr_number, comment['id'])

def reply_to_comment(pr_number, comment_id):
    url = f"{API_URL}/repos/{REPO}/issues/comments"
    payload = {
        'body': "Triggering runtime builds",
        'in_reply_to': comment_id
    }
    response = requests.post(url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=payload)
    response.raise_for_status()
    print(f"Replied to comment {comment_id} on PR #{pr_number}")

if __name__ == "__main__":
    check_mentions_in_comments()
