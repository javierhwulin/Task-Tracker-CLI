import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Annotated

import typer
from rich import print

app = typer.Typer()

TASK_FILE = "tasks.json"


class TaskStatus(str, Enum):
    """Represents the status of a task."""

    ALL = "all"
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"
    OVERDUE = "overdue"


@dataclass
class Task:
    """Represents a single task in the task tracker."""

    id: int
    description: str
    status: TaskStatus
    createdAt: datetime
    updatedAt: datetime
    due: datetime | None


task_list: list[Task] = []
next_id: int = 1

# --- Serialization Helpers ---


def task_to_dict(task: Task) -> dict:
    """
    Convert a Task object into a dictionary for JSON serialization.
    """
    due_date = task.due.isoformat() if task.due is not None else None
    return {
        "id": task.id,
        "description": task.description,
        "status": task.status.value,
        "createdAt": task.createdAt.isoformat(),
        "updatedAt": task.updatedAt.isoformat(),
        "due": due_date,
    }


def task_from_dict(data: dict) -> Task:
    """
    Convert a dictionary into a Task object.
    """
    due_date = datetime.fromisoformat(data["due"]) if data["due"] is not None else None

    return Task(
        id=data["id"],
        description=data["description"],
        status=TaskStatus(data["status"]),
        createdAt=datetime.fromisoformat(data["createdAt"]),
        updatedAt=datetime.fromisoformat(data["updatedAt"]),
        due=due_date,
    )


def save_tasks():
    """
    Save the current task list to a JSON file.
    """
    with open(TASK_FILE, "w") as f:
        json.dump([task_to_dict(task) for task in task_list], f, indent=2)


def load_tasks():
    """
    Load the task list from a JSON file. Sets the next available ID.
    """
    global task_list, next_id
    try:
        with open(TASK_FILE, "r") as f:
            data = json.load(f)
            task_list = [task_from_dict(d) for d in data]
            next_id = max(task.id for task in task_list) + 1 if task_list else 1
    except FileNotFoundError:
        task_list = []
        next_id = 1


# --- CLI Commands ---


@app.command("add")
def add_task(
    description: str = typer.Argument(help="Task description"),
    year: Annotated[int | None, typer.Option(help="Due year")] = None,
    month: Annotated[int | None, typer.Option(help="Due month")] = None,
    day: Annotated[int | None, typer.Option(help="Due day")] = None,
    hour: Annotated[int, typer.Option(help="Due hour")] = 0,
    minute: Annotated[int, typer.Option(help="Due minute")] = 0,
    second: Annotated[int, typer.Option(help="Due second")] = 0,
):
    """
    Add a task with a specified description.
    """
    load_tasks()
    global next_id

    due_date = None
    if year and month and day:
        due_date = datetime(year, month, day, hour or 0, minute or 0, second or 0)

    task = Task(
        id=next_id,
        description=description,
        status=TaskStatus.TODO,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
        due=due_date,
    )
    task_list.append(task)
    save_tasks()
    print(f"[green]Task added successfully (ID: {task.id})[/green]")
    next_id += 1


@app.command("update")
def update_task(
    id: int = typer.Argument(help="Update a task by ID"),
    description: str = typer.Argument(help="Update the task with a new description"),
):
    """
    Update the description of an existing task by ID.
    """
    load_tasks()
    for task in task_list:
        if task.id == id:
            task.description = description
            task.updatedAt = datetime.now()
            save_tasks()
            print(f"[yellow]Task ID {id} updated successfully[/yellow]")
            return
    print(f"[red]Task with ID {id} not found[/red]")


@app.command("delete")
def delete_task(id: int = typer.Argument(help="Delete a task by ID")):
    """
    Delete a task using its ID.
    """
    load_tasks()
    for i, task in enumerate(task_list):
        if task.id == id:
            task_list.pop(i)
            save_tasks()
            print(f"[yellow]Task ID {id} deleted[/yellow]")
            return
    print(f"[red]Task with ID {id} not found[/red]")


@app.command("mark-in-progress")
def mark_in_progress(id: int = typer.Argument(help="Mark the task as in-progress")):
    """
    Update a task's status to 'in-progress'.
    """
    load_tasks()
    for task in task_list:
        if task.id == id:
            task.status = TaskStatus.IN_PROGRESS
            task.updatedAt = datetime.now()
            save_tasks()
            print(f"[green]Task ID {id} marked as in-progress[/green]")
            return
    print(f"[red]Task with ID {id} not found[/red]")


@app.command("mark-done")
def mark_done(id: int = typer.Argument(help="Mark the task as done")):
    """
    Update a task's status to 'done'.
    """
    load_tasks()
    for task in task_list:
        if task.id == id:
            task.status = TaskStatus.DONE
            task.updatedAt = datetime.now()
            save_tasks()
            print(f"[green]Task ID {id} marked as done[/green]")
            return
    print(f"[red]Task with ID {id} not found[/red]")


@app.command("list")
def show(
    status: Annotated[
        TaskStatus, typer.Argument(help="Filter tasks by status (default: all)")
    ] = TaskStatus.ALL,
):
    """
    List tasks, optionally filtering by status.
    """
    load_tasks()
    auto_update_overdue()
    if len(task_list) == 0:
        print("[cyan]No remaining tasks for today[/cyan]")
        return
    if status == TaskStatus.ALL:
        list_all_tasks()
    elif status == TaskStatus.TODO:
        list_todo_tasks()
    elif status == TaskStatus.IN_PROGRESS:
        list_in_progress_tasks()
    elif status == TaskStatus.DONE:
        list_done_tasks()
    elif status == TaskStatus.OVERDUE:
        list_overdue_tasks()
    save_tasks()


# --- Task List Views ---


def list_all_tasks():
    """
    Show all tasks regardless of status.
    """
    print("[bold cyan]All Tasks[/bold cyan]")
    for task in task_list:
        print_task(task)


def list_todo_tasks():
    """
    Show only tasks with status 'todo'.
    """
    print("[cyan]TODO Tasks[/cyan]")
    for task in task_list:
        if task.status == TaskStatus.TODO:
            print_task(task)


def list_in_progress_tasks():
    """
    Show only tasks with status 'in-progress'.
    """
    print("[cyan]In Progress Tasks[/cyan]")
    for task in task_list:
        if task.status == TaskStatus.IN_PROGRESS:
            print_task(task)


def list_done_tasks():
    """
    Show only tasks with status 'done'.
    """
    print("[cyan]Completed Tasks[/cyan]")
    for task in task_list:
        if task.status == TaskStatus.DONE:
            print_task(task)


def list_overdue_tasks():
    """
    Show only tasks with status "overdue".
    """
    print("[cyan]Overdue Tasks[/cyan]")
    for task in task_list:
        if task.status == TaskStatus.OVERDUE:
            print_task(task)


def print_task(task: Task):
    """
    Helper to print a task in a nice format.
    """
    now = datetime.now()

    if task.due is None:
        due_str = "[dim]No due date[/dim]"
    else:
        delta = task.due - now
        if delta.total_seconds() > 0:  # future due date
            # If due date is more than 1 day away, show absolute day
            if delta.total_seconds() >= 86400:
                due_str = f"[italic]Due on {task.due:%Y-%m-%d %H:%M}[/italic]"
            else:
                seconds = int(delta.total_seconds())
                if seconds >= 3600:
                    time_str = f"{seconds // 3600} hour(s)"
                elif seconds >= 60:
                    time_str = f"{seconds // 60} minute(s)"
                else:
                    time_str = f"{seconds} seconds"
                due_str = f"[italic]Due in {time_str}[/italic]"
        else:  # overdue
            seconds = int(abs(delta.total_seconds()))
            if seconds >= 3600:
                time_str = f"{seconds // 3600} hour(s)"
            elif seconds >= 60:
                time_str = f"{seconds // 60} minute(s)"
            else:
                time_str = f"{seconds} seconds"
            due_str = f"[red]Overdue by {time_str}[/red]"
    print(
        f"[white]ID:[/white] {task.id} | "
        f"[bold]{task.description}[/bold] | "
        f"Status: [magenta]{task.status.value}[/magenta] | "
        f"Created: {task.createdAt:%Y-%m-%d %H:%M} | "
        f"Updated: {task.updatedAt:%Y-%m-%d %H:%M} | "
        f"{due_str}"
    )


def auto_update_overdue():
    now = datetime.now()
    for task in task_list:
        if (
            task.due is not None
            and task.due < now
            and task.status not in [TaskStatus.DONE, TaskStatus.OVERDUE]
        ):
            task.status = TaskStatus.OVERDUE


if __name__ == "__main__":
    app()
