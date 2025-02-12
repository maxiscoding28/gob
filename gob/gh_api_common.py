import os
import requests

def build_headers():
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set. Please run the following command in your terminal: export GITHUB_TOKEN=$(gh auth token)")
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    return headers

def handle_response(response):
    """
    Handles the HTTP response from the GitHub API.

    Args:
        response (requests.Response): The response object from the requests library.

    Returns:
        tuple: (request_successful (bool), response_data (dict or list), error_message (str or None))
    """
    if response.ok:  # Checks for 200-299 status codes
        return True, response.json(), None
    elif response.status_code in {400, 401, 403, 404}:
        # Handle client-side errors (invalid input, authentication issues, etc.)
        error_message = f"Client error ({response.status_code}): {response.text}"
        return False, {}, error_message
    elif response.status_code >= 500:
        # Handle server-side errors
        error_message = f"Server error ({response.status_code}): {response.text}"
        return False, {}, error_message
    else:
        # Handle any unexpected response
        error_message = f"Unexpected error ({response.status_code}): {response.text}"
        return False, {}, error_message



class HoustonError(Exception):
    def __init__(self, message):
        self.message = f"🧑‍🚀 Houston, we have a problem: {message}"
        super().__init__(self.message)

def issues_list_url(owner, repository):
    return f"https://api.github.com/repos/{owner}/{repository}/issues"

def list_issues(owner, repository, params=None):
    """
    Fetches the list of issues from the specified repository.

    Args:
        owner (str): The owner of the repository.
        repository (str): The name of the repository.
        params (dict, optional): Additional query parameters for the API request.

    Returns:
        tuple: (request_successful (bool), response_data (list or dict), error_message (str or None))
    """
    url = issues_list_url(owner, repository)
    headers = build_headers()

    # Ensure params is a dictionary, even if None is passed
    params = params or {}

    # Perform the GET request
    response = requests.get(url, headers=headers, params=params)

    # Handle the response based on its status code
    return handle_response(response)

def post_issue_comment(comment_url, comment_data):
    """
    Posts a comment to a specified issue.

    Args:
        comment_url (str): The URL to post the comment to.
        comment_data (dict): The data of the comment to be posted.

    Returns:
        tuple: (request_successful (bool), response_data (dict), error_message (str or None))
    """
    headers = build_headers()

    # Perform the POST request
    response = requests.post(comment_url, headers=headers, json=comment_data)

    return handle_response(response)

