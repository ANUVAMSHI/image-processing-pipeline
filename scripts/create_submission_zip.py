import os
import zipfile

def create_submission_zip():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_path = os.path.join(base_dir, "ANUVAMSHI_BN.zip")

    include_dirs = ["app", "static", "samples", "scripts", "tests"]
    include_files = [
        "Dockerfile",
        "docker-compose.yml",
        "EVALUATION_REPORT.md",
        "README.md",
        "requirements.txt",
        "walkthrough.md",
        "ANUVAMSHI_BN_GitHub_Link.txt",
        ".env.example",
        ".gitignore"
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add directories and all contents recursively
        for dir_name in include_dirs:
            dir_full = os.path.join(base_dir, dir_name)
            if os.path.exists(dir_full):
                for root, dirs, files in os.walk(dir_full):
                    if "__pycache__" in root or ".pytest_cache" in root:
                        continue
                    for file in files:
                        file_full = os.path.join(root, file)
                        rel_path = os.path.relpath(file_full, base_dir)
                        zf.write(file_full, rel_path)

        # Add root files
        for file_name in include_files:
            file_full = os.path.join(base_dir, file_name)
            if os.path.exists(file_full):
                zf.write(file_full, file_name)

    print(f"ANUVAMSHI_BN.zip successfully created at: {zip_path}")

if __name__ == "__main__":
    create_submission_zip()
