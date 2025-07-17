import os

def find_gitignore_files(root_dir):
    """
    Finds all .gitignore files in the given directory and its subdirectories.
    
    Args:
        root_dir (str): The root directory to start searching from.
        
    Returns:
        list: A list of paths to .gitignore files.
    """
    gitignore_files = []
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == '.gitignore':
                full_path = os.path.join(root, file)
                gitignore_files.append(full_path)
    
    return gitignore_files

def main():
    # Get the project directory (change this to your project path)
    project_dir = input("Enter the path to your project directory: ").strip()
    
    # Verify the directory exists
    if not os.path.isdir(project_dir):
        print(f"Error: Directory '{project_dir}' does not exist.")
        return
    
    # Find all .gitignore files
    gitignore_files = find_gitignore_files(project_dir)
    
    # Print results
    if gitignore_files:
        print("\nFound .gitignore files:")
        for i, file_path in enumerate(gitignore_files, 1):
            print(f"{i}. {file_path}")
    else:
        print("No .gitignore files found in the project structure.")

if __name__ == "__main__":
    main() 