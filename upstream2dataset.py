#!/usr/bin/env python3
import requests
import base64
import sys
"""
GitHub Upstream Repository Tree Content Extractor
---------------------------------------------------
Description:
    This script interacts with the GitHub API to retrieve the file tree of a specified repository and branch.
    Writes the content of each file full path and content to a text file, genarally used to create a dataset.

Usage:
    python upstream2dataset.py <repo_name> <branch> <gh_pat>
    Example:
        python3 upstream2dataset.py "github-acc/github-repo" "main" "ghp_zzzzzzzzzzzzzzzzzz"

Prerequisites:
    - Python 3.x
    - The 'requests' library (install via: pip3 install requests)
    - A valid GitHub Personal Access Token (gh_pat) with appropriate permissions.
"""

def get_file_content(file_url, headers):
    """Obtains and decodes the content of a file via the GitHub API."""
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    content_json = response.json()
    decoded_bytes = base64.b64decode(content_json['content'])
    return decoded_bytes.decode('utf-8')

def get_github_repo_tree(repo, branch, headers):
    """Returns the API response containing the repository's directory tree."""
    url = f'https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=true'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'Error in request: {e}')
        return None

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <repo_name> <branch> <gh_pat>")
        print(f"Example: {sys.argv[0]} 'github-acc/github-repo' 'main' 'ghp_zzzzzzzzzzzzzzzzzz'")
        sys.exit(1)
    
    repo = sys.argv[1]
    branch = sys.argv[2]
    gh_pat = sys.argv[3]
    headers = {
        'Authorization': f'token {gh_pat}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    out_file = f"{repo.replace('/', '@')}-{branch}_FullDataset.txt"
    
    response = get_github_repo_tree(repo, branch, headers)
    if not response:
        sys.exit(1)
    data = response.json()
    
    # Filter files whose path contains "examples"
    # target_files = [item for item in data.get('tree', []) if 'examples' in item.get('path', '')]
    # Filter files whose path ends with ".py"
    # target_files = [item for item in data.get('tree', []) if item.get('path', '').endswith('.py')]
    # Filter files whose path contains "src" and ends with ".py"
    # target_files = [item for item in data.get('tree', []) if 'src' in item.get('path', '') and item.get('path', '').endswith('.py')]
    # Filter files whose path contains "src" or "examples"
    # target_files = [item for item in data.get('tree', []) if 'src' in item.get('path', '') or 'examples' in item.get('path', '')]
    # filter all files
    target_files = [item for item in data.get('tree', []) if item.get('path', '')]

    print(f'{len(target_files)} files were found in the project {repo} on branch {branch}')
    print(f'Creating output file {out_file}')
    
    with open(out_file, 'w', encoding='utf-8') as out_f:
        out_f.write(f'Project repo Name: {repo}\n')
        out_f.write(f'Project repo Branch: {branch}\n\n')
        
        for item in target_files:
            if item.get('type') == 'blob':
                print(item.get('path'))
                try:
                    file_content = get_file_content(item['url'], headers)
                except Exception as e:
                    print(f'[-] Error retrieving content for file {item.get("path")}: {e}')
                    continue
                out_f.write(f'File Name: {item["path"]}\n')
                out_f.write(f'File {item["path"]} Content:\n{file_content}\n\n')
    
    print(f'Output file {out_file} created successfully!')

if __name__ == '__main__':
    main()
