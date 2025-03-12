import requests
import json
from datetime import datetime

# GitHub username
USERNAME = "YOUR_GITHUB_USERNAME"
TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"  # Needed for private repo access

# Personal details
SPOKEN_LANGUAGES = ["English", "Hindi"]
PROGRAMMING_LANGUAGES = ["Python", "JavaScript", "Solidity", "C#"]
EMAIL_PERSONAL = "yourpersonal@example.com"
EMAIL_WORK = "yourwork@example.com"
LINKEDIN = "https://linkedin.com/in/YOUR_LINKEDIN"

# GitHub API Headers (for authentication)
HEADERS = {"Authorization": f"token {TOKEN}"}

# GitHub API URLs
GITHUB_API = f"https://api.github.com/users/{USERNAME}"
GITHUB_REPOS_API = f"https://api.github.com/user/repos"
GITHUB_STATS_API = f"https://api.github.com/repos/{USERNAME}/{USERNAME}/stats/contributors"

# Fetch GitHub Profile Data
response = requests.get(GITHUB_API, headers=HEADERS)
if response.status_code == 200:
    data = response.json()

    # GitHub Stats
    created_at = data["created_at"]
    account_age = (datetime.utcnow() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")).days // 365
    total_public_repos = data["public_repos"]
    total_followers = data["followers"]
    total_following = data["following"]

    # Fetch Repositories (Including Private)
    repos_data = requests.get(GITHUB_REPOS_API, headers=HEADERS).json()
    total_private_repos = sum(1 for repo in repos_data if repo["private"])
    total_repos = total_public_repos + total_private_repos
    total_stars = sum(repo["stargazers_count"] for repo in repos_data)
    total_forks = sum(repo["forks_count"] for repo in repos_data)
    total_watchers = sum(repo["watchers_count"] for repo in repos_data)

    # Fetch Commit Stats (Lifetime Commits)
    total_commits = 0
    additions = 0
    deletions = 0

    for repo in repos_data:
        commits_url = f"https://api.github.com/repos/{USERNAME}/{repo['name']}/stats/contributors"
        commit_response = requests.get(commits_url, headers=HEADERS)

        if commit_response.status_code == 200 and commit_response.json():
            for contributor in commit_response.json():
                if contributor["author"]["login"] == USERNAME:
                    total_commits += contributor["total"]
                    for week in contributor["weeks"]:
                        additions += week["a"]
                        deletions += week["d"]

    total_loc = additions - deletions  # Net Lines of Code

    # Generate README Content
    readme_content = f"""
# Hello, I'm {USERNAME}! 👋

## 📌 About Me
- **GitHub Username:** `{USERNAME}`
- **GitHub Account Age:** `{account_age} years`
- **Followers:** `{total_followers}` | **Following:** `{total_following}`

## 📊 GitHub Statistics
| Metric                 | Value |
|------------------------|------------------|
| 🔹 **Total Repositories (Public + Private)** | `{total_repos}` |
| 🔹 **Public Repositories** | `{total_public_repos}` |
| 🔹 **Private Repositories** | `{total_private_repos}` |
| ⭐ **Total Stars Received** | `{total_stars}` |
| 🍴 **Total Forks** | `{total_forks}` |
| 👀 **Total Watchers** | `{total_watchers}` |
| 📌 **Total Commits (Lifetime)** | `{total_commits}` |
| ➕ **Total Lines Added** | `{additions}` |
| ➖ **Total Lines Deleted** | `{deletions}` |
| 🔥 **Net Lines of Code (Added - Deleted)** | `{total_loc}` |

## 🛠️ My Skills & Interests
- **Programming Languages:** {", ".join(PROGRAMMING_LANGUAGES)}
- **Spoken Languages:** {", ".join(SPOKEN_LANGUAGES)}

## 🖥️ My GitHub Stats Dashboard
<div align="center">
  <table>
    <tr>
      <td>
        <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={USERNAME}&hide=html&hide_border=true&layout=compact&langs_count=8&theme=synthwave" alt="Top Languages">
      </td>
      <td>
        <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username={USERNAME}&theme=synthwave&hide_border=true" alt="Repos Per Language">
      </td>
      <td>
        <img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username={USERNAME}&theme=synthwave&hide_border=true" alt="Most Commit Language">
      </td>
    </tr>
  </table>
  <img src="https://github-readme-stats.vercel.app/api?username={USERNAME}&show_icons=true&theme=synthwave" alt="{USERNAME}'s GitHub stats">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username={USERNAME}&theme=synthwave&hide_border=true">
</div>

## 📬 Contact Information
- **Personal Email:** {EMAIL_PERSONAL}
- **Work Email:** {EMAIL_WORK}
- **LinkedIn:** [Click Here]({LINKEDIN})

_Last updated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_  
🚀 *This README updates automatically every 24 hours!*
    """

    # Write to README.md
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

    print("README updated successfully!")

else:
    print("Failed to fetch GitHub data")
