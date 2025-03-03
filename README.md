# upstream2dataset

## Description

**upstream2dataset** is a Python tool that interacts with the GitHub API to extract the directory tree of a specified repository and branch. Its primary goal is to generate a dataset containing the full path and content of each file, facilitating data analysis or processing from upstream repositories.

## Features

- **Repository Tree Extraction:** Retrieves the repository's directory structure recursively using the GitHub API.
- **Content Retrieval:** For each file (blob) found, the tool requests and decodes its content (Base64 encoded).
- **Dataset Generation:** Creates an output file that includes the repository name, branch, and, for each file, its full path and content.
- **Filtering Possibility:** Offers the possibility to filter files according to your requirements.

## Requirements

- **Python 3.x**
- The **requests** library (install via: `pip install requests`)
- A valid **GitHub Personal Access Token (gh_pat)** with the necessary permissions.

## Installation && Usage
```
1. Clone or download this repository to your local machine
$ git clone https://github.com/usrbinbrain/upstream2dataset.git

2. Install the requests library by running pip3.
$ pip3 install requests

3. Run upstream2dataset with args.
$ python3 upstream2dataset/upstream2dataset.py <repository_name> <branch> <gh_pat>
```

#### Parameters:
- **`<repository_name>`:** The repository name in the format `username/repository` (e.g., `oracle/oci-python-sdk`).
- **`<branch>`:** The branch to be explored (e.g., `main` or `master`).
- **`<gh_pat>`:** Your GitHub Personal Access Token.

#### Output .txt

The below command will result in the `github-acc@github-repo-main_FullDataset.txt` output file, written in the local directory of execution.

```bash
python upstream2dataset.py "github-acc/github-repo" "main" "ghp_zzzzzzzzzzzzzzzzzz"
```

Assuming the repository github-acc/github-repo in main branch has the following basic structure:

```
github-acc/github-repo (main)
├── README.md
├── src
│   ├── app.py
│   └── utils.py
└── docs
    └── guide.txt
```

The output file will have an entry for each file, following this pseudo-format:

```
Project repo Name: github-acc/github-repo
Project repo Branch: main

File Name: README.md
File README.md Content:
<file content>

File Name: src/app.py
File src/app.py Content:
<file content>

File Name: src/utils.py
File src/utils.py Content:
<file content>

File Name: docs/guide.txt
File docs/guide.txt Content:
<file content>
```

## Internal Functionality

1. **Repository Tree Request:**  
   The tool constructs the GitHub API URL to access the file tree of the specified repository and branch, utilizing the `recursive=true` parameter to retrieve all directory levels.

2. **File Iteration:**  
   After obtaining the structure, the script iterates over the items to select files (blobs) and requests each file's content.

3. **Decoding and Writing:**  
   The content, originally encoded in Base64, is decoded into text and written to an output file along with the file's full path. The output file is named based on the repository name and branch (e.g., `github-acc@github-repo-main_FullDataset.txt`).

## Customization and Filters

The tool also offers the possibility to apply filtering options, allowing you to process specific files based on your criteria.
