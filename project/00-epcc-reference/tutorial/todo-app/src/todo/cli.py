"""Command-line interface for the todo application."""

import typer
from rich import print
from rich.table import Table

from . import storage

app = typer.Typer(help="Simple todo list manager")


@app.command()
def add(title: str = typer.Argument(..., help="Todo description")) -> None:
    """Add a new todo item."""
    todo = storage.add_todo(title)
    print(f"[green]Added:[/green] {todo.title} [dim]({todo.id})[/dim]")


@app.command("list")
def list_todos(
    all: bool = typer.Option(False, "--all", "-a", help="Include completed items")
) -> None:
    """List todo items."""
    todos = storage.load_todos()

    if not all:
        todos = [t for t in todos if not t.completed]

    if not todos:
        print("[dim]No todos found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Status", width=3)
    table.add_column("ID", style="dim")
    table.add_column("Title")

    for todo in todos:
        status = "[green]\u2713[/green]" if todo.completed else "[ ]"
        table.add_row(status, todo.id, todo.title)

    print(table)
    print(f"\n[dim]{len(todos)} item(s)[/dim]")


@app.command()
def complete(todo_id: str = typer.Argument(..., help="Todo ID to complete")) -> None:
    """Mark a todo item as completed."""
    todo = storage.complete_todo(todo_id)

    if todo:
        print(f"[green]Completed:[/green] {todo.title}")
    else:
        print(f"[red]Error:[/red] Todo '{todo_id}' not found")
        raise typer.Exit(1)


@app.command()
def delete(todo_id: str = typer.Argument(..., help="Todo ID to delete")) -> None:
    """Delete a todo item."""
    # Get the todo first to show its title
    todo = storage.get_todo_by_id(todo_id)

    if todo:
        storage.delete_todo(todo_id)
        print(f"[red]Deleted:[/red] {todo.title}")
    else:
        print(f"[red]Error:[/red] Todo '{todo_id}' not found")
        raise typer.Exit(1)


@app.command()
def clear() -> None:
    """Remove all completed todos."""
    removed = storage.clear_completed()

    if removed > 0:
        print(f"[yellow]Cleared:[/yellow] {removed} completed item(s)")
    else:
        print("[dim]No completed items to clear.[/dim]")


if __name__ == "__main__":
    app()
