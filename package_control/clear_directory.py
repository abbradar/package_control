import os
import stat


def clear_directory(directory, ignore_paths=None):
    """
    Tries to delete all files and folders from a directory

    :param directory:
        The string directory path

    :param ignore_paths:
        An array of paths to ignore while deleting files

    :return:
        If all of the files and folders were successfully deleted
    """

    was_exception = False
    for root, dirs, files in os.walk(directory, topdown=False):
        paths = [os.path.join(root, f) for f in files]
        paths.extend([os.path.join(root, d) for d in dirs])

        for path in paths:
            try:
                # Don't delete the metadata file, that way we have it
                # when the reinstall happens, and the appropriate
                # usage info can be sent back to the server
                if ignore_paths and path in ignore_paths:
                    continue
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    try:
                        if os.name == 'nt' and not os.access(path, os.W_OK):
                            try:
                                os.chmod(path, stat.S_IWUSR)
                            except (PermissionError):
                                pass
                        os.remove(path)
                    except OSError:
                        # try to rename file to reduce chance that
                        # file is in use on next start
                        os.rename(path, path + '.old')
                        raise
            except (OSError, IOError):
                was_exception = True

    return not was_exception
