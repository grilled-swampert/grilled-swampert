import requests
import json
import os
from datetime import datetime

# GitHub Username & Token
USERNAME = os.environ("GITHUB_USERNAME")  # Replace with your actual username
GITHUB_TOKEN = os.environ("GITHUB_TOKEN")  # Replace with your personal access token

# Personal details
SPOKEN_LANGUAGES = ["English", "Hindi"]  # Update as needed
PROGRAMMING_LANGUAGES = ["Python", "JavaScript", "Solidity", "C#"]  # Update as needed
EMAIL_PERSONAL = "yourpersonal@example.com"
EMAIL_WORK = "yourwork@example.com"
LINKEDIN = "https://linkedin.com/in/YOUR_LINKEDIN"

# GraphQL Query
GRAPHQL_QUERY = """
{
  viewer {
    login
    name
    bio
    createdAt
    repositories(first: 100, ownerAffiliations: OWNER) {
      totalCount
      nodes {
        name
        stargazers {
          totalCount
        }
        forks {
          totalCount
        }
        primaryLanguage {
          name
        }
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 1) {
                totalCount
              }
            }
          }
        }
        size
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
    followers {
      totalCount
    }
    following {
      totalCount
    }
    pullRequests(first: 100) {
      totalCount
    }
    issues(first: 100) {
      totalCount
    }
  }
}
"""

# Send GraphQL Request
response = requests.post(
    "https://api.github.com/graphql",
    json={"query": GRAPHQL_QUERY},
    headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
)

if response.status_code == 200:
    data = response.json()["data"]["viewer"]

    # Account Stats
    created_at = data["createdAt"]
    account_age = (datetime.utcnow() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")).days // 365
    total_repos = data["repositories"]["totalCount"]
    total_followers = data["followers"]["totalCount"]
    total_following = data["following"]["totalCount"]
    total_contributions = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    total_pull_requests = data["pullRequests"]["totalCount"]
    total_issues = data["issues"]["totalCount"]

    # Aggregate repo statistics
    total_stars = sum(repo["stargazers"]["totalCount"] for repo in data["repositories"]["nodes"])
    total_forks = sum(repo["forks"]["totalCount"] for repo in data["repositories"]["nodes"])
    total_commits = sum(repo["defaultBranchRef"]["target"]["history"]["totalCount"] for repo in data["repositories"]["nodes"] if repo["defaultBranchRef"])
    total_loc = sum(repo["size"] * 100 for repo in data["repositories"]["nodes"])  # Approximate LOC

    # Most used languages
    language_count = {}
    for repo in data["repositories"]["nodes"]:
        lang = repo["primaryLanguage"]
        if lang:
            language_count[lang["name"]] = language_count.get(lang["name"], 0) + 1
    top_languages = sorted(language_count.items(), key=lambda x: x[1], reverse=True)[:5]  # Top 5 languages

    # Generate README Content
    readme_content = f"""
# Hello, I'm {USERNAME}! 👋

## 🌟 GitHub Stats
- **GitHub Age:** {account_age} years
- **Repositories:** {total_repos}
- **Stars:** {total_stars}
- **Forks:** {total_forks}
- **Commits:** {total_commits}
- **Contributions:** {total_contributions}
- **Pull Requests:** {total_pull_requests}
- **Issues Opened:** {total_issues}
- **Lines of Code on GitHub:** {total_loc}

## 🛠️ Skills & Interests
- **Programming Languages:** {", ".join(PROGRAMMING_LANGUAGES)}
- **Most Used GitHub Languages:** {", ".join([lang[0] for lang in top_languages])}
- **Spoken Languages:** {", ".join(SPOKEN_LANGUAGES)}

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
    print("Failed to fetch GitHub data:", response.text)
