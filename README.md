
# Folder Synchronization Script

## Description

This Python script performs one-way synchronization between two folders, copying files from the **source folder** to the **replica folder**. It also removes files from the replica that no longer exist in the source. Synchronizations happen at defined intervals, and all operations are logged in a log file.

## Usage
Run the program:
   ```bash
   python sync.py <source_folder> <replica_folder> <interval_in_seconds> <log_file_path>
   ```

   - `<source_folder>`: Path to the source folder.
   - `<replica_folder>`: Path to the replica folder.
   - `<interval_in_seconds>`: Interval in seconds between synchronizations.
   - `<log_file_path>`: Path to the log file.

### Example:
```bash
python3 task.py test test_replica 5 logs.txt
```

In this case, the program will create the `test_replica` folder, which will be our replica folder, and it will create the `logs.txt` file. It will then copy all the files from `test` to `test_replica`, performing synchronization every 5 seconds and executing the necessary operations if there have been any changes.

## How It Works

- **Periodic synchronization**: Every X seconds, the replica will be updated to mirror the source.
- **Replica folder and log file creation**: The script automatically creates the replica folder and log file if they do not exist.
- **Operation logging**: All actions (file creation, copying, and deletion) are printed in the terminal and logged in the specified log file.

## Requirements

- Python 3.x
