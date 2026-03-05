#!/usr/bin/env python3
import requests
import base64
import sys
import json

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
        print(f"Usage: {sys.argv[0]} <repo_name> <branch> <gh_pat> [txt|json]")
        print(f"Example TXT:  {sys.argv[0]} 'github-acc/github-repo' 'main' 'ghp_xxx'")
        print(f"Example JSON: {sys.argv[0]} 'github-acc/github-repo' 'main' 'ghp_xxx' json")
        sys.exit(1)

    repo = sys.argv[1]
    branch = sys.argv[2]
    gh_pat = sys.argv[3]
    output_format = sys.argv[4].lower() if len(sys.argv) >= 5 else 'txt'

    if output_format not in ('txt', 'json'):
        print("Invalid output format. Use 'txt' or 'json'.")
        sys.exit(1)

    headers = {
        'Authorization': f'token {gh_pat}',
        'Accept': 'application/vnd.github.v3+json'
    }

    extension = 'json' if output_format == 'json' else 'txt'
    out_file = f"{repo.replace('/', '@')}-{branch}_FullDataset.{extension}"

    response = get_github_repo_tree(repo, branch, headers)
    if not response:
        sys.exit(1)
    data = response.json()

    print(data)

    target_files = [item for item in data.get('tree', []) if item.get('path', '')]
    print(f'{len(target_files)} files were found in the project {repo} on branch {branch}')
    print(f'Creating output file {out_file}')

    files_data = []
    for item in target_files:
        if item.get('type') == 'blob':
            print(item.get('path'))
            try:
                file_content = get_file_content(item['url'], headers)
            except Exception as e:
                print(f'[-] Error retrieving content for file {item.get("path")}: {e}')
                continue

            files_data.append({
                'path': item['path'],
                'content': file_content,
                'sha': item['sha'],
                'size': item['size']
            })

    if output_format == 'json':
        payload = {
            'repo': repo,
            'branch': branch,
            'files': files_data
        }
        with open(out_file, 'w', encoding='utf-8') as out_f:
            json.dump(payload, out_f, ensure_ascii=False, indent=2)
    else:
        with open(out_file, 'w', encoding='utf-8') as out_f:
            out_f.write(f'Project repo Name: {repo}\n')
            out_f.write(f'Project repo Branch: {branch}\n\n')
            for file_item in files_data:
                out_f.write(f'File Name: {file_item["path"]}\n')
                out_f.write(f'File {file_item["path"]} Content:\n{file_item["content"]}\n\n')

    print(f'Output file {out_file} created successfully!')

if __name__ == '__main__':
    main()