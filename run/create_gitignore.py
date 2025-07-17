gitignore_content = """
# DuckDB database files
*.duckdb

# Python cache
__pycache__/
*.py[cod]

# Environment
.env
.venv/
"""

with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gitignore_content.strip())
