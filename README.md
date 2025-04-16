# Task Tracker CLI

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/javierhwulin/Task-Tracker-CLI)](https://github.com/javierhwulin/Task-Tracker-CLI/commits/main)
[![Open Issues](https://img.shields.io/github/issues/javierhwulin/Task-Tracker-CLI)](https://github.com/javierhwulin/Task-Tracker-CLI/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/javierhwulin/Task-Tracker-CLI)](https://github.com/javierhwulin/Task-Tracker-CLI/pulls)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)](#)
[![Platform](https://img.shields.io/badge/Platform-CLI-lightgrey.svg)](#)

A simple CLI-based task tracker built with [Typer](https://typer.tiangolo.com/) and [Rich](https://github.com/Textualize/rich) for managing to-do items in a JSON file.
Inspired by 

## About the Project

This task tracker is a command-line application that allows you to manage tasks in a simple JSON file. You can add tasks, update them, mark them as in-progress or done, list them based on status, and delete them entirely — all from the comfort of your terminal. This project aims to be a quick, lightweight way to track small to medium to-do lists without needing a large database or web interface.

### Key Features

- **Add Tasks:** Quickly add tasks from your CLI, with an auto-incremented ID.
- **Mark Tasks:** Mark tasks as `in-progress` or `done` to keep track of your progress.
- **Update/Delete Tasks:** Update descriptions or remove tasks that you no longer need.
- **Filter by Status:** List tasks by their status (`todo`, `in-progress`, `done`) or list all.

### Tech Stack

- **Python 3.9+**: The primary programming language.
- **Typer**: A user-friendly command-line interface library.
- **Rich**: Provides colored output and formatting for improved readability.
- **JSON File**: Used for simple data storage (no external database required).

## Getting Started

Below you’ll find instructions on setting up and running the task tracker on your local machine.

### Prerequisites

- **Python 3.9+** (earlier versions may work, but this app was tested on 3.9+)
- [Pip](https://pypi.org/project/pip/) (usually bundled with Python)
- (Optional) [Virtualenv](https://pypi.org/project/virtualenv/) if you prefer to keep dependencies isolated

### Installation

1. **Clone the Repository**:

```bash
git clone https://github.com/javierhwulin/Task-Tracker-CLI.git
```

2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
This will install Typer, Rich, and any other required dependencies.

### Examples

1. **Add a Task**  
    ~~~bash
    python main.py add "Buy groceries"
    ~~~
    **Output**:
    ```
    Task added successfully (ID: 1)
    ```
   
2. **List All Tasks**  
    ~~~bash
    python main.py list
    ~~~
    **Output**:
    ```
    All Tasks
    ID: 1 | Buy groceries | Status: todo | Created: 2025-04-15 13:45
    ```
   
3. **Update a Task**  
    ~~~bash
    python main.py update 1 "Buy groceries (milk, eggs, bread)"
    ~~~
    **Output**:
    ```
    Task ID 1 updated successfully
    ```
   
4. **Mark Task In-Progress**  
    ~~~bash
    python main.py mark-in-progress 1
    ~~~
    **Output**:
    ```
    Task ID 1 marked as in-progress
    ```
   
5. **Mark Task as Done**  
    ~~~bash
    python main.py mark-done 1
    ~~~
    **Output**:
    ```
    Task ID 1 marked as done
    ```
   
6. **Delete a Task**  
    ~~~bash
    python main.py delete 1
    ~~~
    **Output**:
    ```
    Task ID 1 deleted
    ```

### Additional Commands

- **Help**:  
    ~~~bash
    python main.py --help
    ~~~
    or
    ~~~bash
    python main.py [COMMAND] --help
    ~~~
    Displays Typer’s help screen with usage details for each command.

## Roadmap

- [x] **Support for Due Dates**: Add the ability to assign due dates to tasks and filter them accordingly.
- [ ] **Recurring Tasks**: Automatically re-create tasks after a set interval (daily, weekly, monthly).
- [ ] **Task Prioritization**: Allow labeling tasks with priorities (low, medium, high).
- [ ] **Improved Output Formatting**: Potentially integrate more Rich formatting features (like tables) for better readability.


## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

## Contact

**Javier Hengda** – [javier.hwulin.devtech@gmail.com](mailto:javier.hwulin.devtech@gmail.com)  

## Acknowledgements
- Project idea from [roadmap.sh](https://roadmap.sh/projects/task-tracker)
- [Typer](https://typer.tiangolo.com/) for the awesome CLI framework.
- [Rich](https://github.com/Textualize/rich) for making terminal output look fabulous.
- The open-source community for fostering collaboration.

## Support

If you encounter any problems or have suggestions, feel free to [open an issue](https://github.com/javierhwulin/Task-Tracker-CLI/issues). You can also reach out via email if the issue is more personal or complex.

