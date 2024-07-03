"""
Actions manager for Composio SDK.

Usage:
    composio actions [command] [options]
"""

import typing as t

import click
from composio.utils.enums import get_enum_key
import pyperclip
import json

from composio.cli.context import Context, pass_context
from composio.cli.utils.helpfulcmd import HelpfulCmdBase
from composio.client.enums import App, Action
from composio.core.cls.did_you_mean import DYMGroup
from composio.exceptions import ComposioSDKError


class ActionsExamples(HelpfulCmdBase, DYMGroup):
    examples = [
        click.style("composio actions", fg="green")
        + click.style(
            "                                    # List all actions\n", fg="black"
        ),
        click.style("composio actions --app slack", fg="green")
        + click.style(
            "                        # List all actions for the Slack app\n", fg="black"
        ),
        click.style("composio actions --use-case 'get channel messages'", fg="green")
        + click.style(
            "  # List all actions for the 'get channel messages' use case\n", fg="black"
        ),
        click.style(
            "composio actions execute 'action_name' --params '{\"key\": \"value\"}'",
            fg="green",
        )
        + click.style("  # Execute a specific action with parameters\n", fg="black"),
    ]


@click.group(name="actions", invoke_without_command=True, cls=ActionsExamples)
@click.help_option("--help", "-h", "-help")
@click.option(
    "--app",
    "apps",
    type=str,
    multiple=True,
    help="Filter by app name",
)
@click.option(
    "--tag",
    "tags",
    type=str,
    multiple=True,
    help="Filter by given tag",
)
@click.option(
    "--use-case",
    "use_case",
    type=str,
    help="Filter by app name",
)
@click.option(
    "--limit",
    "limit",
    type=int,
    default=10,
    help="Limit the number of actions to show",
)
@click.option(
    "--enabled",
    is_flag=True,
    default=False,
    help="Only show actions which are enabled",
)
@click.option(
    "--copy",
    "copy_enums",
    is_flag=True,
    default=False,
    help="Copy actions as a list of `Action` enum instances.",
)
@pass_context
def _actions(
    context: Context,
    apps: t.Sequence[str],
    tags: t.Sequence[str],
    use_case: t.Optional[str] = None,
    limit: int = 10,
    enabled: bool = False,
    copy_enums: bool = False,
) -> None:
    """List composio actions"""
    if context.click_ctx.invoked_subcommand:
        return

    if use_case is not None and len(apps) == 0:
        raise click.ClickException(
            "To search by a use case you need to specify atleast one app name."
        )
    try:
        actions = context.client.actions.get(
            apps=[App(app) for app in apps],
            use_case=use_case,
            allow_all=True,
            limit=limit,
        )
        if enabled:
            actions = [integration for integration in actions if integration.enabled]
            context.console.print("[green]Showing actions which are enabled[/green]")
        else:
            context.console.print("[green]Showing all actions[/green]")

        enum_strs = []
        for action in actions:
            if len(tags) > 0 and all(tag not in action.tags for tag in tags):
                continue
            enum_strs.append(f"Action.{get_enum_key(name=action.name)}")
            context.console.print(f"• {action.name} ({enum_strs[-1]})")

        if len(tags) > 0 and len(enum_strs) == 0:
            raise click.ClickException(
                f"Could not find actions with following tags {set(tags)}"
            )

        if copy_enums or (
            click.prompt(
                "Do you copy these actions as enums?",
                type=click.Choice(
                    choices=("y", "n"),
                    case_sensitive=False,
                ),
            )
            == "y"
        ):
            pyperclip.copy(text="[" + ", ".join(enum_strs) + "]")

    except ComposioSDKError as e:
        raise click.ClickException(message=e.message) from e


@_actions.command(name="execute")
@click.argument("action_name", type=str)
@click.option("--params", "-p", type=str, help="Action parameters as a JSON string")
@pass_context
def execute(context: Context, action_name: str, params: str) -> None:
    """Execute a Composio action"""
    try:
        # Parse JSON parameters
        action_params = json.loads(params) if params else {}
        # Execute the action
        result = context.client.actions.execute(Action(action_name), action_params)
        context.console.print(result)

    except json.JSONDecodeError:
        raise click.ClickException("Invalid JSON format for parameters")
    except ComposioSDKError as e:
        raise click.ClickException(message=e.message) from e
