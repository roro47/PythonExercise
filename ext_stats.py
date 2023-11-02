#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path

import click


def get_all_files_in_path(path: Path, recursive: bool):
    for f in path.iterdir():
        if f.is_file():
            yield f
        elif recursive and f.is_dir():
            yield from get_all_files_in_path(f, recursive)


@click.command()
@click.option("-r", "--recursive", is_flag=True, default=False, help="")
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, path_type=Path),
)
def ext_stats(directory: Path, recursive: bool):
    """
    Show extension statistics for all files in a directory. The program collects,
    by file extension, these statistics:

    \b
    1. the number of files with each extension
    2. the size in bytes of the largest file with each extension
    3. the total file size in bytes of all files with each extension
    """

    files = get_all_files_in_path(directory, recursive)
    ext_count = defaultdict(int)
    ext_max_filesize = defaultdict(int)
    ext_total_filesize = defaultdict(int)

    extension_column_space = 0
    count_column_space = 0
    max_filesize_column_space = 0
    total_filesize_column_space = 0

    for f in files:
        ext = f.suffix or "<no ext>"
        file_size = f.stat().st_size
        ext_count[ext] += 1
        ext_total_filesize[ext] += file_size
        ext_max_filesize[ext] = max(ext_max_filesize[ext], file_size)

        extension_column_space = max(extension_column_space, len(ext))
        count_column_space = max(count_column_space, len(str(ext_count[ext])))
        max_filesize_column_space = max(max_filesize_column_space, len(str(file_size)))
        total_filesize_column_space = max(
            total_filesize_column_space, len(str(ext_total_filesize[ext]))
        )

    for ext, count in ext_count.items():
        print(
            ext.ljust(extension_column_space),
            str(count).rjust(count_column_space),
            str(ext_max_filesize[ext]).rjust(max_filesize_column_space),
            str(ext_total_filesize[ext]).rjust(total_filesize_column_space),
        )


if __name__ == "__main__":
    ext_stats()
