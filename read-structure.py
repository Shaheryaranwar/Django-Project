import os

def generate_project_structure(start_path, output_file="project_structure.txt"):
    """
    Generates a text file showing the complete folder and file structure of a project.
    
    Args:
        start_path (str): Root directory of your project
        output_file (str): Name of the output text file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for root, dirs, files in os.walk(start_path):
                level = root.replace(start_path, '').count(os.sep)
                indent = ' ' * 4 * level
                f.write(f"{indent}{os.path.basename(root)}/\n")
                
                subindent = ' ' * 4 * (level + 1)
                for file in files:
                    f.write(f"{subindent}{file}\n")
        
        print(f"\nProject structure successfully saved to: {os.path.abspath(output_file)}")
        print(f"Total size: {os.path.getsize(output_file)} bytes")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Configure these settings
    PROJECT_ROOT = "E:\Cloudchain_Project\Shopinzo\blossom.shopinzo.io"  # Change this to your project path
    OUTPUT_FILENAME = "front_project_structure.txt"     # Change if you want different filename
    
    print(f"Generating project structure for: {PROJECT_ROOT}")
    generate_project_structure(PROJECT_ROOT, OUTPUT_FILENAME)
    
    # Optional: Open the file automatically after creation
    if os.name == 'nt':  # For Windows
        os.startfile(OUTPUT_FILENAME)
    else:  # For Mac/Linux
        os.system(f'open "{OUTPUT_FILENAME}"' if sys.platform == 'darwin' else f'xdg-open "{OUTPUT_FILENAME}"')