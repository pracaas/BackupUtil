import csv
import tempfile
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

from DataSafeGuard import safe_guard_ledger, DataSafeGuard


class TestDataSafeGuard(TestCase):

    def test_should_get_source_and_destination_from_ledger(self):
        ledger_file = tempfile.NamedTemporaryFile(suffix="ledger.csv")

        # Write the data to the CSV file
        with open(ledger_file.name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(("Source", "Destination"))
            writer.writerow(("source/path", "destination/path"))

        mocked_method = Mock()
        obj = DataSafeGuard()
        with patch.object(obj, 'take_backup', new=mocked_method):
            safe_guard_ledger(ledger_file.name, mocked_method)

        print("Number of calls to the mock:", mocked_method.take_backup.call_count)
        call_args = mocked_method.take_backup.call_args
        print("Arguments passed to the mock:", call_args.args)
        self.assertEqual(call_args.args, ("source/path", "destination/path"))

    def test_should_get_multiple_sources_and_destinations_from_ledger(self):
        ledger_file = tempfile.NamedTemporaryFile(suffix="ledger.csv")

        # Write the data to the CSV file
        with open(ledger_file.name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(("Source", "Destination"))
            writer.writerow(("source1/path", "destination1/path"))
            writer.writerow(("source2/path", "destination2/path"))

        mocked_method = Mock()
        obj = DataSafeGuard()
        with patch.object(obj, 'take_backup', new=mocked_method):
            safe_guard_ledger(ledger_file.name, mocked_method)

        print("Number of calls to the mock:", mocked_method.take_backup.call_count)
        call_args = mocked_method.take_backup.call_args
        print("Arguments passed to the mock:", call_args.args)
        self.assertEqual(mocked_method.take_backup.call_count, 2)
        self.assertEqual(mocked_method.method_calls[0].args, ("source1/path", "destination1/path"))
        self.assertEqual(mocked_method.method_calls[1].args, ("source2/path", "destination2/path"))

    def test_should_not_take_backup_when_external_drive_is_not_mounted(self):
        ledger_file = tempfile.NamedTemporaryFile(suffix="ledger.csv")

        # Write the data to the CSV file
        with open(ledger_file.name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(("Source", "Destination"))
            writer.writerow(("source1/path", "/Volumes/Factory/path"))

        mocked_method = Mock()
        obj = DataSafeGuard()
        with patch.object(obj, 'take_backup', new=mocked_method):
            safe_guard_ledger(ledger_file.name, mocked_method)

        print("Number of calls to the mock:", mocked_method.take_backup.call_count)
        self.assertEqual(mocked_method.take_backup.call_count, 0)

    def test_should_take_next_backup_when_failure_occurs(self):
        ledger_file = tempfile.NamedTemporaryFile(suffix="ledger.csv")

        # Write the data to the CSV file
        # given I have two backup task
        with open(ledger_file.name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(("Source", "Destination"))
            writer.writerow(("source1/path", "destination1/path"))
            writer.writerow(("source2/path", "destination2/path"))

        def side_effect(source, destination):
            if source == "source1/path" and destination == "destination1/path":
                raise FileNotFoundError("File Not Found!")
            else:
                return None

        obj = MagicMock()
        obj.take_backup.side_effect = side_effect

        # when safeguard takes backup
        safe_guard_ledger(ledger_file.name, obj)

        # then all the backup task should be attempted.
        print("Number of calls to the mock:", obj.take_backup.call_count)
        call_args = obj.take_backup.call_args
        print("Arguments passed to the mock:", call_args.args)
        self.assertEqual(obj.take_backup.call_count, 2)
