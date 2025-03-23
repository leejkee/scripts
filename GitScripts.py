import argparse
import subprocess

def run_command(command):
    """Run Git command"""
    process = subprocess.run(command, shell=True)

def main():
    parser = argparse.ArgumentParser(description="Git Commit Script")
    parser.add_argument("-m", required=True, help="commit message")
    parser.add_argument("-b", default="main", help="branch name")

    args = parser.parse_args()
    branch = args.b
    commit_message = args.m

    print("\nGit Commit Script\n")
    
    print("1. Add all files to staging area")
    run_command("git add .")

    print("2. Commit changes")
    run_command(f'git commit -m "{commit_message}"')

    print("3. Push changes to remote repository on branch", branch)
    run_command(f"git push origin {branch}")

    print("\nGit Commit Script completed successfully\n")

if __name__ == "__main__":
    main()
