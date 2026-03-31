"""Main CLI entry point using click + rich."""

from __future__ import annotations

import asyncio
import json
import os
import sys
from functools import wraps
from typing import Any, Callable

import click
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

from hubspot_sdk import HubSpotClient

console = Console()


def get_token() -> str:
    token = os.environ.get("HUBSPOT_ACCESS_TOKEN") or os.environ.get("HUBSPOT_API_KEY")
    if not token:
        console.print("[red]Error:[/red] Set HUBSPOT_ACCESS_TOKEN environment variable")
        sys.exit(1)
    return token


def async_command(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to run an async click command."""

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def print_objects(results: list[dict[str, Any]], properties: list[str] | None = None) -> None:
    """Print a list of HubSpot objects as a rich table."""
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim")

    # Determine columns from first result
    if properties:
        cols = properties
    else:
        sample_props = results[0].get("properties", {})
        cols = list(sample_props.keys())[:8]  # limit to 8 columns

    for col in cols:
        table.add_column(col)

    for obj in results:
        props = obj.get("properties", {})
        row = [obj.get("id", "")]
        for col in cols:
            row.append(str(props.get(col, "")))
        table.add_row(*row)

    console.print(table)


def print_json(data: Any) -> None:
    """Print data as syntax-highlighted JSON."""
    text = json.dumps(data, indent=2, default=str)
    console.print(Syntax(text, "json", theme="monokai"))


# ============================================================================
# Top-level CLI group
# ============================================================================


@click.group()
@click.version_option(package_name="hubspot-sdk")
def cli() -> None:
    """HubSpot CLI – manage your HubSpot data from the command line."""


# ============================================================================
# Contacts
# ============================================================================


@cli.group()
def contacts() -> None:
    """Manage contacts."""


@contacts.command("list")
@click.option("--limit", default=10, help="Number of results")
@click.option("--properties", "-p", multiple=True, help="Properties to include")
@click.option("--after", default=None, help="Pagination cursor")
@click.option("--json-output", is_flag=True, help="Output raw JSON")
@async_command
async def contacts_list(limit: int, properties: tuple[str, ...], after: str | None, json_output: bool) -> None:
    """List contacts."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.contacts.list(
            limit=limit,
            properties=list(properties) if properties else None,
            after=after,
        )
        if json_output:
            print_json(result.model_dump(mode="json"))
        else:
            print_objects([r.model_dump(mode="json") for r in result.results], list(properties) if properties else None)
            if result.has_next:
                console.print(f"\n[dim]Next page: --after {result.next_after}[/dim]")


@contacts.command("get")
@click.argument("contact_id")
@click.option("--properties", "-p", multiple=True)
@async_command
async def contacts_get(contact_id: str, properties: tuple[str, ...]) -> None:
    """Get a single contact by ID."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.contacts.get(
            contact_id, properties=list(properties) if properties else None
        )
        print_json(result.model_dump(mode="json"))


@contacts.command("create")
@click.option("--prop", "-p", multiple=True, type=(str, str), help="Property name and value")
@async_command
async def contacts_create(prop: tuple[tuple[str, str], ...]) -> None:
    """Create a contact."""
    props = {k: v for k, v in prop}
    async with HubSpotClient(get_token()) as hs:
        result = await hs.contacts.create(props)
        console.print(f"[green]Created contact {result.id}[/green]")
        print_json(result.model_dump(mode="json"))


@contacts.command("update")
@click.argument("contact_id")
@click.option("--prop", "-p", multiple=True, type=(str, str))
@async_command
async def contacts_update(contact_id: str, prop: tuple[tuple[str, str], ...]) -> None:
    """Update a contact."""
    props = {k: v for k, v in prop}
    async with HubSpotClient(get_token()) as hs:
        result = await hs.contacts.update(contact_id, props)
        console.print(f"[green]Updated contact {result.id}[/green]")


@contacts.command("delete")
@click.argument("contact_id")
@async_command
async def contacts_delete(contact_id: str) -> None:
    """Archive a contact."""
    async with HubSpotClient(get_token()) as hs:
        await hs.contacts.delete(contact_id)
        console.print(f"[green]Archived contact {contact_id}[/green]")


@contacts.command("search")
@click.option("--query", "-q", default=None, help="Full-text search query")
@click.option("--filter", "-f", multiple=True, type=(str, str, str), help="property operator value")
@click.option("--limit", default=10)
@click.option("--properties", "-p", multiple=True)
@async_command
async def contacts_search(query: str | None, filter: tuple[tuple[str, str, str], ...], limit: int, properties: tuple[str, ...]) -> None:
    """Search contacts."""
    filter_groups = []
    if filter:
        filters = []
        for prop_name, operator, value in filter:
            filters.append({"propertyName": prop_name, "operator": operator, "value": value})
        filter_groups = [{"filters": filters}]

    async with HubSpotClient(get_token()) as hs:
        result = await hs.contacts.search(
            query=query,
            filter_groups=filter_groups if filter_groups else None,
            properties=list(properties) if properties else None,
            limit=limit,
        )
        console.print(f"[dim]Total: {result.total}[/dim]")
        print_objects([r.model_dump(mode="json") for r in result.results], list(properties) if properties else None)


# ============================================================================
# Companies
# ============================================================================


@cli.group()
def companies() -> None:
    """Manage companies."""


@companies.command("list")
@click.option("--limit", default=10)
@click.option("--properties", "-p", multiple=True)
@click.option("--json-output", is_flag=True)
@async_command
async def companies_list(limit: int, properties: tuple[str, ...], json_output: bool) -> None:
    """List companies."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.companies.list(limit=limit, properties=list(properties) if properties else None)
        if json_output:
            print_json(result.model_dump(mode="json"))
        else:
            print_objects([r.model_dump(mode="json") for r in result.results], list(properties) if properties else None)


@companies.command("get")
@click.argument("company_id")
@async_command
async def companies_get(company_id: str) -> None:
    """Get a company by ID."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.companies.get(company_id)
        print_json(result.model_dump(mode="json"))


@companies.command("create")
@click.option("--prop", "-p", multiple=True, type=(str, str))
@async_command
async def companies_create(prop: tuple[tuple[str, str], ...]) -> None:
    """Create a company."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.companies.create({k: v for k, v in prop})
        console.print(f"[green]Created company {result.id}[/green]")


# ============================================================================
# Deals
# ============================================================================


@cli.group()
def deals() -> None:
    """Manage deals."""


@deals.command("list")
@click.option("--limit", default=10)
@click.option("--properties", "-p", multiple=True)
@click.option("--json-output", is_flag=True)
@async_command
async def deals_list(limit: int, properties: tuple[str, ...], json_output: bool) -> None:
    """List deals."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.deals.list(limit=limit, properties=list(properties) if properties else None)
        if json_output:
            print_json(result.model_dump(mode="json"))
        else:
            print_objects([r.model_dump(mode="json") for r in result.results], list(properties) if properties else None)


@deals.command("get")
@click.argument("deal_id")
@async_command
async def deals_get(deal_id: str) -> None:
    """Get a deal by ID."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.deals.get(deal_id)
        print_json(result.model_dump(mode="json"))


@deals.command("create")
@click.option("--prop", "-p", multiple=True, type=(str, str))
@async_command
async def deals_create(prop: tuple[tuple[str, str], ...]) -> None:
    """Create a deal."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.deals.create({k: v for k, v in prop})
        console.print(f"[green]Created deal {result.id}[/green]")


@deals.command("search")
@click.option("--query", "-q")
@click.option("--limit", default=10)
@click.option("--properties", "-p", multiple=True)
@async_command
async def deals_search(query: str | None, limit: int, properties: tuple[str, ...]) -> None:
    """Search deals."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.deals.search(
            query=query, limit=limit, properties=list(properties) if properties else None
        )
        console.print(f"[dim]Total: {result.total}[/dim]")
        print_objects([r.model_dump(mode="json") for r in result.results])


# ============================================================================
# Tickets
# ============================================================================


@cli.group()
def tickets() -> None:
    """Manage tickets."""


@tickets.command("list")
@click.option("--limit", default=10)
@click.option("--properties", "-p", multiple=True)
@async_command
async def tickets_list(limit: int, properties: tuple[str, ...]) -> None:
    """List tickets."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.tickets.list(limit=limit, properties=list(properties) if properties else None)
        print_objects([r.model_dump(mode="json") for r in result.results])


@tickets.command("create")
@click.option("--prop", "-p", multiple=True, type=(str, str))
@async_command
async def tickets_create(prop: tuple[tuple[str, str], ...]) -> None:
    """Create a ticket."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.tickets.create({k: v for k, v in prop})
        console.print(f"[green]Created ticket {result.id}[/green]")


# ============================================================================
# Objects (generic)
# ============================================================================


@cli.group("objects")
def objects_group() -> None:
    """Manage any CRM object type."""


@objects_group.command("list")
@click.argument("object_type")
@click.option("--limit", default=10)
@click.option("--properties", "-p", multiple=True)
@async_command
async def objects_list(object_type: str, limit: int, properties: tuple[str, ...]) -> None:
    """List objects of any type."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.objects(object_type).list(
            limit=limit, properties=list(properties) if properties else None
        )
        print_objects([r.model_dump(mode="json") for r in result.results])


@objects_group.command("get")
@click.argument("object_type")
@click.argument("object_id")
@async_command
async def objects_get(object_type: str, object_id: str) -> None:
    """Get any object by type and ID."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.objects(object_type).get(object_id)
        print_json(result.model_dump(mode="json"))


@objects_group.command("create")
@click.argument("object_type")
@click.option("--prop", "-p", multiple=True, type=(str, str))
@async_command
async def objects_create(object_type: str, prop: tuple[tuple[str, str], ...]) -> None:
    """Create any object."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.objects(object_type).create({k: v for k, v in prop})
        console.print(f"[green]Created {object_type} {result.id}[/green]")


@objects_group.command("search")
@click.argument("object_type")
@click.option("--query", "-q")
@click.option("--limit", default=10)
@async_command
async def objects_search(object_type: str, query: str | None, limit: int) -> None:
    """Search any object type."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.objects(object_type).search(query=query, limit=limit)
        console.print(f"[dim]Total: {result.total}[/dim]")
        print_objects([r.model_dump(mode="json") for r in result.results])


# ============================================================================
# Files
# ============================================================================


@cli.group("files")
def files_group() -> None:
    """Manage files."""


@files_group.command("list")
@click.option("--limit", default=10)
@async_command
async def files_list(limit: int) -> None:
    """List files."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.files.list(limit=limit)
        print_json(result)


@files_group.command("upload")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--folder", default="/", help="Target folder path")
@async_command
async def files_upload(file_path: str, folder: str) -> None:
    """Upload a file to HubSpot."""
    import mimetypes

    filename = os.path.basename(file_path)
    mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        async with HubSpotClient(get_token()) as hs:
            result = await hs.files.upload(
                files={"file": (filename, f, mime)},
                data={
                    "options": json.dumps({
                        "access": "PUBLIC_NOT_INDEXABLE",
                    }),
                    "folderPath": folder,
                },
            )
    console.print(f"[green]Uploaded: {filename}[/green]")
    print_json(result)


# ============================================================================
# Pipelines
# ============================================================================


@cli.group("pipelines")
def pipelines_group() -> None:
    """Manage pipelines."""


@pipelines_group.command("list")
@click.argument("object_type")
@async_command
async def pipelines_list(object_type: str) -> None:
    """List pipelines for an object type (e.g., deals, tickets)."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.pipelines.list(object_type)
        print_json(result)


# ============================================================================
# Properties
# ============================================================================


@cli.group("properties")
def properties_group() -> None:
    """Manage object properties."""


@properties_group.command("list")
@click.argument("object_type")
@async_command
async def properties_list(object_type: str) -> None:
    """List properties for an object type."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.properties.list(object_type)
        if "results" in result:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Name")
            table.add_column("Label")
            table.add_column("Type")
            table.add_column("Field Type")
            for prop in result["results"]:
                table.add_row(
                    prop.get("name", ""),
                    prop.get("label", ""),
                    prop.get("type", ""),
                    prop.get("fieldType", ""),
                )
            console.print(table)
        else:
            print_json(result)


# ============================================================================
# Owners
# ============================================================================


@cli.group("owners")
def owners_group() -> None:
    """Manage CRM owners."""


@owners_group.command("list")
@async_command
async def owners_list() -> None:
    """List all owners."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.owners.list()
        print_json(result)


# ============================================================================
# Account
# ============================================================================


@cli.group("account")
def account_group() -> None:
    """Account info and settings."""


@account_group.command("info")
@async_command
async def account_info() -> None:
    """Get account details."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.account_info.get_details()
        print_json(result)


@account_group.command("api-usage")
@async_command
async def account_api_usage() -> None:
    """Get API usage stats."""
    async with HubSpotClient(get_token()) as hs:
        result = await hs.account_info.get_api_usage()
        print_json(result)


if __name__ == "__main__":
    cli()
