# IBKR Flex Queries Downloader

A tool to download Interactive Brokers Flex Queries reports.

---

## Features

-   Add, list, and delete credentials (name, token, query ID) via CLI
-   Run downloads silently via CLI with `--silent` flag
-   GUI launches when run without any flags
-   Saves individual reports in the `reports/` folder
-   Merges CSV reports into a single combined file

---

## Requirements

-   Python 3.11+
-   Dependencies listed in `requirements.txt`

---

## Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Show help:

```bash
python main.py -h
```

Add new credential:

```bash
python main.py add --name "MyAccount" --token YOUR_TOKEN --query-id YOUR_QUERY_ID
```

List credentials:

```bash
python main.py list
```

Delete credential:

```bash
python main.py delete --name "MyAccount"
```

Download reports:

```bash
python main.py --silent
```

Start GUI:

```bash
python main.py
```

---

## Releases

Pre-built executables are available for download in the [GitHub Releases](https://github.com/DrSans69/IBKR-flex-query-downloader) section.

-   **Windows:** `main.exe`

### Running the executable

```bash
./main.exe
```

---

## File Structure

-   credentials.csv — stores saved tokens and query IDs
-   reports/ — downloaded individual report CSV files
-   logs/ — application log files
-   src/ — source code modules

---

## Logging

Logs are saved to logs/app.log
They have max size and backups
