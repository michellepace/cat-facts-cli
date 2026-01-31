# Python Project Template

![Banner showing uv package manager logo plus Python logo equals "Python ready to go"](x_docs/images/readme-banner.jpg)

A [uv](https://docs.astral.sh/uv/)-based Python 3.14+ project template configured for test-driven development (pytest) and code quality checks (Ruff, Pyright). These run automatically every time you commit.

Supports development in [`src/`](src/) packages, standalone [`scripts/`](scripts/), and Jupyter [`notebooks/`](notebooks/). Complete IDE setup included for VSCode/Cursor ([extensions](.vscode/extensions.json), [settings](.vscode/settings.json)).

## 📁 Project Structure

Key project directories and files:

| | Name | Description |
|:-:|------|-------------|
| 📂 | [.claude/](.claude/) | Claude Code configuration and project instructions |
| 📂 | .venv/ | Virtual environment created by `uv sync` (gitignored) |
| 📂 | [.vscode/](.vscode/) | [extensions](.vscode/extensions.json) for VSCode/Cursor and IDE [settings](.vscode/settings.json) |
| 📂 | [notebooks/](notebooks/) | Jupyter notebooks |
| 📂 | [scripts/](scripts/) | Standalone utility scripts |
| 📂 | [src/uv_python_template/](src/uv_python_template/) | Package source code |
| 📂 | [tests/](tests/) | Test files mirroring src/ structure |
| 📄 | [.gitattributes](.gitattributes) | Git line-ending, diff, and notebook filter settings |
| 📄 | [.gitignore](.gitignore) | Files excluded from version control |
| 📄 | [.markdownlint.yaml](.markdownlint.yaml) | Markdown linting configuration |
| 📄 | [.pre-commit-config.yaml](.pre-commit-config.yaml) | Automated quality checks before each commit |
| 📄 | [.python-version](.python-version) | Python version specification for uv |
| 📄 | [pyproject.toml](pyproject.toml) | Project dependencies and tool configuration |
| 📄 | [README.md](README.md) | This file |
| 📄 | [uv.lock](uv.lock) | Dependency versions (do not edit manually) |

## 📦 Installation

1. Prerequisite: install the uv Python package manager [from here](https://docs.astral.sh/uv/getting-started/installation/)

2. Clone the repository to "my-project-name"

   ```bash
    git clone https://github.com/michellepace/uv-python-template.git my-project-name
   ```

3. Run these terminal commands for first-time setup:

    ```bash
    # Change directory into new project
    cd my-project-name

    # Install project dependencies (creates .venv/ directory)
    uv sync

    # Install pre-commit hooks (runs quality checks before each commit)
    uv run pre-commit install
    ```

4. Open "my-project-name" in your IDE and open a new terminal (so it picks up the virtual environment):
   - Run `which python` → should show a path ending in `.venv/bin/python`
   - Run `uv run pre-commit run --all-files` → linting, type checking, and tests should pass

5. Install the recommended extensions from [.vscode/extensions.json](.vscode/extensions.json). These are already configured in [.vscode/settings.json](.vscode/settings.json).

6. Open [`notebooks/example.ipynb`](notebooks/example.ipynb), select the `.venv` Python interpreter, and run it.

   <div align="center">
     <a href="notebook_pic.jpg">
       <img src="notebook_pic.jpg" alt="VS Code screenshot showing example.ipynb notebook with project code integration. The notebook demonstrates importing from uv_python_template.play and testing the add() function with successful output. Pink arrows point to the kernel selector in the top right, with 'select' annotation indicating where to choose the Python 3.14 (.venv) environment." width="600">
     </a>
     <p><em>Project Structure (left) with Jupyter Notebook (right)</em></p>
   </div>

7. [Set up Jupyter Git integration (Recommended)](#-jupyter-notebook-git-integration-recommended) — keeps notebook outputs out of version control while preserving them locally.

## 📓 Jupyter Notebook Git Integration (Recommended)

This project uses [nbstripout](https://github.com/kynan/nbstripout) to keep notebooks clean in Git. It automatically strips cell outputs and metadata when committing, so you get:

- **Cleaner diffs** — only code changes, not output noise
- **Smaller repos** — no large binary outputs bloating history
- **Fewer merge conflicts** — outputs don't clash between branches
- **No re-running after commits** — your local notebook keeps its outputs; only the version sent to Git is stripped

**One-time global setup** (works for all your current and future repos with notebooks):

```bash
# Install nbstripout as a global uv tool
uv tool install nbstripout

# Configure Git to use it globally
nbstripout --install --global

# To remove later: nbstripout --uninstall --global && uv tool uninstall nbstripout
```

Any repo with `*.ipynb filter=nbstripout` in `.gitattributes` (like this one) will now automatically strip outputs on commit.

## ✨ Make It Yours

Use AI prompts to quickly adapt this template to your project:

1. Instruct AI (renaming): *Refactor this project to consistently rename it from "uv-python-template" to "my-project-name" throughout. Use `git mv` for renaming!*

2. Instruct AI (changes): *I will not be using Jupyter notebooks in this project. Remove all notebook-related files, references, and dependencies throughout.*

3. Manually refine [.claude/CLAUDE.md](.claude/CLAUDE.md) to suit your preferences and project.
