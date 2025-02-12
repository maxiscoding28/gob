import click
import webbrowser
import re
from .gh_api_common import list_issues, post_issue_comment, HoustonError

@click.group()
def wu():
    """Manage weekly updates."""
    pass

@wu.command('get')
def get_latest_weekly_update():
    """Get the latest weekly update issue."""
    click.echo("Running gob wu get...")
    try:
        questions_of_the_week, _ = get_latest_weekly_update_issue(get_params=False)
    except HoustonError as e:
        click.secho(f"Error: {e}", fg='red')

@wu.command('post')
def post_weekly_update():
    """Post a weekly update."""
    click.echo("Running gob wu post...")
    try:
        questions_of_the_week, comment_url = get_latest_weekly_update_issue(get_params=True)
        questions = [
            "**Your response to the question of the week (QOTW)**",
            "**Do you have any accounts at risk?**",
            "**What other challenges are you working on?**",
            "**What did you learn this week that others should know? Is it worth reduxing?**",
            "**Anything else that's on your mind?**",
            "**Any upcoming time off?**",
            "**Any L&D?**"
        ]
        static_question = "**How have you been this week?**"
        static_response = "Chillin' 🤙"
        responses = [static_question, static_response]
        click.echo("Questions of the Week:")
        for qotw in questions_of_the_week:
            click.echo(f"📆 {qotw}")
        click.echo("\n")
        for question in questions:
            responses.append(question)  # Add the question itself
            response = click.prompt(f"❓ {question}")
            responses.append(response)  # Add the user's response
        comment_data = {
            "body": "\n".join(responses)
        }
        success, _, error = post_issue_comment(comment_url, comment_data)
        if success:
            click.secho("✅ Request Was Successful", fg='green')
        else:
            click.secho(f"Error: {error}", fg='red')
    except HoustonError as e:
        click.secho(f"Error: {e}", fg='red')

def get_latest_weekly_update_issue(get_params=False):
    # Fetch issues with the `since` parameter and sorted by created date in descending order with label team-meeting
    success, issues, error = list_issues(
        "github",
        "premium-support",
        params={
            "since": "2025-01-01T00:00:00Z",
            "sort": "created",
            "direction": "desc",
            "labels": "team-meeting"
        }
    )
    if success:
        if issues and len(issues) > 0:
            latest_weekly_update_issue = issues[0]
            if get_params:
                 questions_of_the_week = re.findall(r'(?:QOTW|BONUS QOTW):\s*"([^"]+)"', latest_weekly_update_issue["body"])
                 comments_url = latest_weekly_update_issue["comments_url"]
                 return questions_of_the_week, comments_url
            else:
                click.echo("🎉 Latest Team Meeting Issue found. Re-run with wu post to update.")
                click.echo(f"🔗 Attempting to open: {latest_weekly_update_issue['html_url']}...")
                webbrowser.open_new_tab(issues[0]["html_url"])
                return [], ""
        else:
            raise HoustonError("No issues found for this week.")
    else:
        raise HoustonError(error)

if __name__ == "__main__":
    wu()