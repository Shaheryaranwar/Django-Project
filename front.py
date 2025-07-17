import os
from pathlib import Path

def generate_vite_structure(project_path, output_file="vite_project_structure.txt"):
    """
    Generates a complete structure of a Vite.js project in a text file.
    
    Args:
        project_path (str): Path to the Vite.js project root
        output_file (str): Name of the output text file
    """
    # Common Vite directories/files to highlight
    VITE_SPECIAL_FILES = {
        'vite.config.js': '⚙️ Vite Config',
        'package.json': '📦 Package Config',
        'src/main.js': '🚀 Main Entry',
        'src/main.ts': '🚀 Main Entry',
        'src/App.vue': '🖥️ Main App',
        'src/App.jsx': '🖥️ Main App',
        'src/App.tsx': '🖥️ Main App',
        'public/': '🌐 Public Assets',
        'node_modules/': '📦 Dependencies (excluded by default)'
    }

    # Common directories to exclude
    EXCLUDE_DIRS = {'node_modules', '.git', '.vscode', '.idea', 'dist', 'build'}

    try:
        project_path = Path(project_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"📂 Vite.js Project Structure: {project_path}\n")
            f.write(f"Generated: {os.path.basename(project_path)}\n\n")
            
            for root, dirs, files in os.walk(project_path):
                # Remove excluded directories
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                
                level = root.replace(str(project_path), '').count(os.sep)
                indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
                
                # Write directory line
                rel_path = os.path.relpath(root, project_path)
                if rel_path == '.':
                    f.write(f"{project_path.name}/\n")
                else:
                    dir_name = os.path.basename(root)
                    special_mark = VITE_SPECIAL_FILES.get(f"{dir_name}/", "")
                    f.write(f"{indent}{dir_name}/{special_mark}\n")
                
                # Write files
                sub_indent = '│   ' * level + '├── '
                for file in sorted(files):
                    file_path = os.path.join(rel_path, file)
                    special_mark = VITE_SPECIAL_FILES.get(file_path, "")
                    
                    # Highlight important files
                    if file_path in VITE_SPECIAL_FILES:
                        emoji = VITE_SPECIAL_FILES[file_path].split()[0]
                        f.write(f"{sub_indent}{emoji} {file} {special_mark[len(emoji)+1:]}\n")
                    elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                        f.write(f"{sub_indent}📜 {file}\n")
                    elif file.endswith('.vue'):
                        f.write(f"{sub_indent}🟢 {file}\n")
                    elif file.endswith('.css'):
                        f.write(f"{sub_indent}🎨 {file}\n")
                    elif file.endswith('.json'):
                        f.write(f"{sub_indent}📄 {file}\n")
                    else:
                        f.write(f"{sub_indent}{file}\n")
            
            # Add Vite-specific summary
            f.write("\n=== Vite Project Summary ===\n")
            f.write("Structure includes:\n")
            f.write("- src/        : Your source code\n")
            f.write("- public/     : Static assets\n")
            f.write("- node_modules: Dependencies (excluded)\n")
            f.write("- vite.config.js: Vite configuration\n")
            
        print(f"✅ Successfully generated Vite project structure in {output_file}")
        print(f"📁 Location: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Configure your Vite project path here
    VITE_PROJECT_PATH = input("Enter your Vite project path: ").strip() or "."
    
    # Output filename
    OUTPUT_FILE = "vite_project_structure.txt"
    
    generate_vite_structure(VITE_PROJECT_PATH, OUTPUT_FILE)
    
    # Try to open the file automatically
    try:
        if os.name == 'nt':
            os.startfile(OUTPUT_FILE)
        else:
            os.system(f'open "{OUTPUT_FILE}"' if sys.platform == 'darwin' else f'xdg-open "{OUTPUT_FILE}"')
    except:
        pass