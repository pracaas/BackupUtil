import csv
import shutil

from DiskUtil import is_mounted
from logger import log


class DataSafeGuard:
    def take_backup(self, src: str, dest: str):
        log.info("Taking backup from %s to %s", src, dest)
        shutil.copytree(src, dest, dirs_exist_ok=True)
        log.info("Back-upped successfully")


def safe_guard_ledger(ledger_path, data_safe_guard: DataSafeGuard):
    with open(ledger_path, mode='r') as file:
        reader = csv.reader(file)

        # Get the header row
        header = next(reader)

        # Find the index of the desired columns
        source_index = header.index("Source")
        dest_index = header.index("Destination")

        # Read the first row and extract values from the desired columns
        log.info("reading ledger data")
        for row in reader:
            source_path = row[source_index]
            destination_path = row[dest_index]
            log.info("Source Path: %s", source_path)
            log.info("Destination Path: %s", destination_path)
            log.info("checking the destination drive is mounted...")
            if is_mounted(destination_path):
                try:
                    data_safe_guard.take_backup(source_path, destination_path)
                except Exception as e:
                    log.error("Exception occurred while copying Source Path: %s, to Destination Path: %s.\nException "
                              "Message: %s", source_path, destination_path, e)
            else:
                log.error("Destination Drive is not mounted: %s", destination_path)


if __name__ == "__main__":
    # Specify the file path for source and destination directories
    source_destination_file_path = "data_transfer_ledger.csv"

    log.info("Test log message")
    # Call the backup function with the specified source and destination file
    backup_obj = DataSafeGuard()
    safe_guard_ledger(source_destination_file_path, backup_obj)