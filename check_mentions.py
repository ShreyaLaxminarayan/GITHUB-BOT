import os
import requests
import subprocess

repo_owner = "dotnet"  
repo_name = "runtime"    
bot_username = "mybot"    

pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"

comments_url_template = "https://api.github.com/repos/{}/{}/issues/{}/comments"

github_token = secrets.
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}

def check_mentions_and_merge():
    response = requests.get(pr_url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching pull requests: {response.status_code}")
        return

    pr_data = response.json()

    for pr in pr_data:
        if pr["state"] == "open":
            pr_number = pr["number"]
            print(f"Checking PR #{pr_number}: {pr['title']}")

            comments_url = comments_url_template.format(repo_owner, repo_name, pr_number)
            comments_response = requests.get(comments_url, headers=headers)
            if comments_response.status_code != 200:
                print(f"Error fetching comments for PR #{pr_number}: {comments_response.status_code}")
                continue

            comments = comments_response.json()

            for comment in comments:
                if f"@{bot_username}" in comment["body"]:
                    print(f"Found mention of @{bot_username} in PR #{pr_number} (comment by {comment['user']['login']}): {comment['body']}")

                    clone_and_merge_repo(pr)

def clone_and_merge_repo(pr):
    pr_number = pr["number"]
    pr_branch = pr["head"]["ref"]  
    
    repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"
    clone_dir = "/tmp/repo"  
    print(f"Cloning repository {repo_url} into {clone_dir}")
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

    os.chdir(clone_dir)

    subprocess.run(["git", "checkout", "main"], check=True)

    subprocess.run(["git", "fetch"], check=True)

    print(f"Merging PR branch {pr_branch} into main")
    subprocess.run(["git", "merge", f"origin/{pr_branch}"], check=True)

    print("Pushing changes to the repository")
    subprocess.run(["git", "push", "origin", "main"], check=True)

    print(f"PR #{pr_number} merged and pushed to main.")

if __name__ == "__main__":
    check_mentions_and_merge()
