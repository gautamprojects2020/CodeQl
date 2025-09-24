import json, pathlib, re

out_dir = pathlib.Path("sql_extracted")
out_dir.mkdir(exist_ok=True)

for nb_file in pathlib.Path(".").rglob("*.ipynb"):
    with open(nb_file, encoding="utf-8") as f:
        nb = json.load(f)

    sql_snippets = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            src = "".join(cell.get("source", []))
            # Look for `%sql` or %%sql magics
            if re.match(r"^\s*%{1,2}sql", src, re.IGNORECASE):
                # Strip the magic command, keep the SQL
                sql = re.sub(r"^\s*%{1,2}sql\s*", "", src, flags=re.IGNORECASE)
                sql_snippets.append(sql.strip())

    if sql_snippets:
        out_file = out_dir / (nb_file.stem + ".sql")
        out_file.write_text("\n\n-- NEXT CELL --\n\n".join(sql_snippets))
        print(f"Extracted SQL from {nb_file} -> {out_file}")
