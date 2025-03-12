import requests
import json
from datetime import datetime

# GitHub username
USERNAME = "grilled-swampert"

# Personal details
SPOKEN_LANGUAGES = ["English", "Hindi"]  # Update as needed
PROGRAMMING_LANGUAGES = ["Python", "JavaScript", "Solidity", "C#"]  # Update as needed
EMAIL_PERSONAL = "yourpersonal@example.com"
EMAIL_WORK = "yourwork@example.com"
LINKEDIN = "https://linkedin.com/in/YOUR_LINKEDIN"

# GitHub API URLs
GITHUB_API = f"https://api.github.com/users/{USERNAME}"
GITHUB_REPOS_API = f"https://api.github.com/users/{USERNAME}/repos"
GITHUB_EVENTS_API = f"https://api.github.com/users/{USERNAME}/events"

# Fetch GitHub Profile Data
response = requests.get(GITHUB_API)
if response.status_code == 200:
    data = response.json()

    # GitHub Stats
    created_at = data["created_at"]
    account_age = (datetime.utcnow() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")).days // 365
    total_repos = data["public_repos"]
    total_followers = data["followers"]
    total_following = data["following"]
    name = data["name"]
    bio = data["bio"]
    blog = data["blog"]

    # Fetch repositories data
    repos_data = requests.get(GITHUB_REPOS_API).json()
    total_stars = sum(repo["stargazers_count"] for repo in repos_data)
    total_forks = sum(repo["forks_count"] for repo in repos_data)
    total_watchers = sum(repo["watchers_count"] for repo in repos_data)

    # Fetch commit count
    commit_count = 0
    try:
        events_data = requests.get(GITHUB_EVENTS_API).json()
        commit_count = sum(1 for event in events_data if event["type"] == "PushEvent")
    except:
        pass  # Skip if error fetching events

    # Fetch total contributions
    total_contributions = sum(
        repo["open_issues_count"] for repo in repos_data
    )  # Approximation for contributions

    # Compute total lines of code (approximate using repo sizes)
    total_loc = sum(repo["size"] for repo in repos_data) * 100  # Approximate LOC

    # Generate README Content
    readme_content = f"""
# Hello, I'm {name or USERNAME}! 👋

## 📌 About Me
- **GitHub Username:** {USERNAME}
- **Bio:** {bio if bio else 'No bio available'}
- **Blog:** {blog if blog else 'No blog available'}
- **GitHub Account Age:** {account_age} years (Since {created_at.split('T')[0]})
- **Followers:** {total_followers} | **Following:** {total_following}

## 📊 GitHub Stats
- **Public Repositories:** {total_repos}
- **Total Stars:** {total_stars}
- **Total Forks:** {total_forks}
- **Total Watchers:** {total_watchers}
- **Total Commits:** {commit_count}
- **Total Contributions:** {total_contributions} (Approximation based on open issues)
- **Lines of Code on GitHub (Approx):** {total_loc}

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

    """

    # Write to README.md
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

    print("README updated successfully!")

else:
    print("Failed to fetch GitHub data")
