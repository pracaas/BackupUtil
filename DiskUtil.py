import os

import psutil


def is_mounted(path):
    # Check if the path corresponds to a mounted volume
    try:
        if "Volumes" in path:
            # Normalize the path and split into components
            path_components = os.path.normpath(path).split(os.path.sep)

            # Find the first component that is 'Volumes'
            volumes_index = path_components.index('Volumes')

            # Reconstruct the root path within /Volumes
            root_mounted_path = os.path.join('/', *path_components[:volumes_index + 2])

            return psutil.os.path.ismount(root_mounted_path)
        return True
    except AttributeError:
        return False