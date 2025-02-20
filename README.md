
# Code LLM Learner

A tool to ingest a codebase, process it, and use an LLM to suggest modifications.

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py --repo <repo-url-or-path> --instruction "Your instruction"`

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Example
```bash
python main.py --repo ./examples/simple_project --instruction "Add error handling"
