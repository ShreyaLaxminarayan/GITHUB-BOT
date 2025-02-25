import os
from github import Github

GITHUB_TOKEN = os.getenv('PAT_TOKEN')

g = Github(GITHUB_TOKEN)

user = g.get_user()
username = user.login
print(username)
repo_name = "saitama951/runtime"
print(f"Repository exists: {repo_name}")

notifications = g.get_repo(repo_name).get_notifications(all=True)

mentioned_prs = []

for notification in notifications:
    if notification.reason == 'mention':
        print("yes")
        if notification.subject.type == 'PullRequest':
            pr_url = notification.subject.url
            pr_number = int(pr_url.split('/')[-1])
            pr = g.get_repo(repo_name).get_pull(pr_number)
            mentioned_prs.append(pr)

# if mentioned_prs:
#    print(mentioned_prs)
#    for pr in mentioned_prs:
#      print(f"PR '{pr.title}' has mentioned you!")
#    else:
#     print("No PR mentions found.")

if mentioned_prs:
    with open(os.getenv("GITHUB_WORKSPACE") + "/pr_numbers.txt", "a") as f:  
        for pr in mentioned_prs:
            f.write(f"PR #{pr.number}\n")
    print(f"Successfully appended {len(mentioned_prs)} PR(s) to the file.")
else:
    print("No PR mentions found.")
