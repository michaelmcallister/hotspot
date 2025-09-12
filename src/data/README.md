# Hotspot SQLite Database

## Developer Documentation

### Requirements

You'll need `sqlite3` installed.

On macOS you can install it with Homebrew (if not already installed)

```
brew install sqlite
```

On Linux, use your system package manager, e.g.:

```
sudo apt-get install sqlite3
```

### Building the Database

The Makefile will generate a SQLite database (`hotspot.db`) from a schema file and CSV datasets.  

Run:
```
make
```

This will:
1. Create a temporary SQLite database.
2. Apply the schema from `create_tables.txt`.
3. Import the CSV files into tables automatically (table name = CSV file name without extension).
4. Rename the temporary database to `hotspot.db`.

### Rebuilding the Database

If you need to rebuild from scratch:

```
make rebuild
```

This will remove the old database and regenerate it.

### Cleaning Up

To remove the generated database:

```
make clean
```

### CSV Imports

The following CSVs are imported:
- `default_risk.csv` → `default_risk` table
- `model_risk.csv` → `model_risk` table
- `postcode_risk.csv` → `postcode_risk` table

> **Note**: The Makefile automatically infers the table name from the CSV filename.

### Verifying the Database

After building, you can explore the database interactively:

```
sqlite3 hotspot.db
```

For example, to list tables:

```
.tables
```

And to inspect a schema:

```
.schema <table_name>
```


