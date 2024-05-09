import hashlib
import os
import tempfile
from unittest import TestCase
import time

from DataSafeGuard import DataSafeGuard


class TestDataSafeGuard(TestCase):

    @staticmethod
    def calculate_checksum(file_path, algorithm='sha256', chunk_size=8192):
        # Open the file and create a hash object
        hasher = hashlib.new(algorithm)

        # Read the file in chunks and update the hash
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                hasher.update(chunk)

        # Return the hexadecimal representation of the digest
        return hasher.hexdigest()

    def test_should_copy_empty_directory(self):
        source_dir = tempfile.mkdtemp()
        folder_path = os.path.join(source_dir, "empty directory")
        os.makedirs(folder_path)
        destination_dir = tempfile.mkdtemp(suffix="destination")

        DataSafeGuard().take_backup(source_dir, destination_dir)

        self.assertTrue(os.path.exists(os.path.join(destination_dir, "empty directory")))


    def test_should_copy_directory_with_file(self):
        source_dir = tempfile.mkdtemp()
        folder_path = os.path.join(source_dir, "empty directory")
        os.makedirs(folder_path)
        file_path = os.path.join(folder_path, "file_name.txt")
        with open(file_path, 'w') as file:
            file.write("This is some content for the file.")
        destination_dir = tempfile.mkdtemp(suffix="destination")

        DataSafeGuard().take_backup(source_dir, destination_dir)
        file_path = os.path.join(destination_dir, "empty directory", "file_name.txt")
        self.assertTrue(os.path.exists(file_path))

    def test_should_copy_a_file(self):
        source_dir = tempfile.mkdtemp()
        src_file_path = os.path.join(source_dir, "file_name.txt")
        with open(src_file_path, 'w') as file:
            file.write("This is some content for the file.")
        destination_dir = tempfile.mkdtemp(suffix="destination")

        DataSafeGuard().take_backup(source_dir, destination_dir)
        dest_file_path = os.path.join(destination_dir, "file_name.txt")
        self.assertTrue(os.path.exists(dest_file_path))
        self.assertEqual(self.calculate_checksum(src_file_path), self.calculate_checksum(dest_file_path))

    def test_should_overwrite_a_file_when_content_is_changed(self):
        source_dir = tempfile.mkdtemp()
        src_file_path = os.path.join(source_dir, "file_name.txt")
        with open(src_file_path, 'w') as file:
            file.write("This is some content for the file.")

        destination_dir = tempfile.mkdtemp(suffix="destination")
        dest_file_path = os.path.join(destination_dir, "file_name.txt")

        with open(dest_file_path, 'w') as file:
            file.write("This is some content for the file.")

        append_time = time.ctime(os.path.getmtime(dest_file_path))

        with open(src_file_path, 'a') as file:
            file.write("This is some content appended for the file.")

        DataSafeGuard().take_backup(source_dir, destination_dir)
        self.assertTrue(os.path.exists(dest_file_path))
        self.assertEqual(self.calculate_checksum(src_file_path), self.calculate_checksum(dest_file_path))

    def test_should_not_overwrite_a_file_when_content_is_same(self):
        # Given I have a file A with some content to be backed up
        source_dir = tempfile.mkdtemp()
        src_file_path = os.path.join(source_dir, "file_name.txt")
        with open(src_file_path, 'w') as file:
            file.write("This is some content for the file.")

        # And I have the same file A which is backed up already
        destination_dir = tempfile.mkdtemp(suffix="destination")
        dest_file_path = os.path.join(destination_dir, "file_name.txt")
        with open(dest_file_path, 'w') as file:
            file.write("This is some content for the file.")

        mtime_before = time.ctime(os.path.getmtime(dest_file_path))
        atime_before = time.ctime(os.path.getatime(dest_file_path))

        time.sleep(3)
        # When I run  take_backup using data safeguard
        DataSafeGuard().take_backup(source_dir, destination_dir)

        dest_file_path_after = os.path.join(destination_dir, "file_name.txt")
        # Then I make sure the file is not overwritten
        self.assertTrue(os.path.exists(dest_file_path))
        mtime_after = time.ctime(os.path.getmtime(dest_file_path_after))
        atime_after = time.ctime(os.path.getatime(dest_file_path_after))
        self.assertEqual(mtime_after, mtime_before)

    def test_should_not_overwrite_a_file_inside_a_folder_when_content_is_same(self):
        # Given I have a file A with some content to be backed up
        source_dir = tempfile.mkdtemp()
        nested_folder = os.path.join(source_dir, "nested directory")
        os.makedirs(nested_folder)
        src_file_path = os.path.join(nested_folder, "file_name.txt")
        with open(src_file_path, 'w') as file:
            file.write("This is some content for the file.")

        # And I have the same file A which is backed up already
        destination_dir = tempfile.mkdtemp(suffix="destination")
        dest_nested_folder = os.path.join(destination_dir, "nested directory")
        os.makedirs(dest_nested_folder)
        dest_file_path = os.path.join(dest_nested_folder, "file_name.txt")
        with open(dest_file_path, 'w') as file:
            file.write("This is some content for the file.")

        mtime_before = time.ctime(os.path.getmtime(dest_file_path))

        time.sleep(3)
        # When I run DataSafeGuard().take_backup
        DataSafeGuard().take_backup(source_dir, destination_dir)

        # Then I make sure the file is not overwritten
        dest_file_path_after = os.path.join(dest_nested_folder, "file_name.txt")
        self.assertTrue(os.path.exists(dest_file_path))
        mtime_after = time.ctime(os.path.getmtime(dest_file_path_after))
        self.assertEqual(mtime_after, mtime_before)