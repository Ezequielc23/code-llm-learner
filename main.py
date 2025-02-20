import argparse
import os
import time
from git import Repo
from src.ingest import import_repo, read_codebase
from src.preprocess import preprocess_code
from src.store import store_chunks, retrieve_context
from src.llm import setup_llm, modify_code

def apply_changes(repo_path, file_path, new_content):
    """Apply changes to the file and commit them."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    repo = Repo(repo_path)
    repo.git.add(file_path)
    repo.git.commit(m="Applied modification suggested by xAI API")
    print(f"Changes committed to {file_path}")

def main():
    parser = argparse.ArgumentParser(description="LLM Codebase Learner with xAI API")
    parser.add_argument("--repo", required=True, help="Repo URL or local path")
    parser.add_argument("--instruction", help="Instruction for code change")
    parser.add_argument("--api-key", required=True, help="xAI API key")
    args = parser.parse_args()

    # Ingest and preprocess
    repo_path = import_repo(args.repo)
    codebase = read_codebase(repo_path)
    chunks = preprocess_code(codebase)
    collection = store_chunks(chunks)

    if args.instruction:
        # Set up xAI API client
        client, model_name = setup_llm(args.api_key)
        context = retrieve_context(args.instruction, collection)
        full_context = "\n".join(context)
        result = modify_code(client, model_name, full_context, args.instruction)
        
        # Display the suggested modification
        print("Suggested modification:\n", result)
        
        # Ask for user approval
        approval = input("Do you want to apply this modification? (y/n): ").strip().lower()
        if approval == "y":
            # Create a new branch with timestamp
            repo = Repo(repo_path)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            branch_name = f"testing_{timestamp}"
            repo.git.checkout("-b", branch_name)
            print(f"Created and switched to branch: {branch_name}")

            # Apply changes to the most relevant file (simplified: assumes first chunk’s file)
            target_file = chunks[0]["file"]  # This could be improved with better file selection logic
            apply_changes(repo_path, target_file, result)
        else:
            print("Modification discarded.")

if __name__ == "__main__":
    main()
    