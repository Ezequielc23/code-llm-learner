import argparse
from src.ingest import import_repo, read_codebase
from src.preprocess import preprocess_code
from src.store import store_chunks, retrieve_context
from src.llm import setup_llm, modify_code

def main():
    parser = argparse.ArgumentParser(description="LLM Codebase Learner")
    parser.add_argument("--repo", required=True, help="Repo URL or local path")
    parser.add_argument("--instruction", help="Instruction for code change")
    args = parser.parse_args()

    # Ingest and preprocess
    repo_path = import_repo(args.repo)
    codebase = read_codebase(repo_path)
    chunks = preprocess_code(codebase)
    collection = store_chunks(chunks)

    if args.instruction:
        # Retrieve context and modify
        llm = setup_llm()
        context = retrieve_context(args.instruction, collection)
        result = modify_code(llm, "\n".join(context), args.instruction)
        print("Suggested modification:\n", result)

if __name__ == "__main__":
    main()
