"""Cluster software setup."""

import os
import errno
import shutil
import argparse

MODULEFILE_TEMPLATE = """--- Metadata
-- Installed by: Matthew Hartley <Matthew.Hartley@jic.ac.uk>
-- From: singularity build
-- License: N/A
-- Test:

whatis("Version: {program_version}")
whatis("Keywords: {program_name}")
whatis("Description: {program_name}")


-- Set the paths
prepend_path("PATH", "{program_path}")

"""

SOFTWARE_ROOT = "/jic/software/testing"
MODULEFILE_ROOT = "/common/modulefiles/Core"
SINGULARITY_ROOT = "/usr/users/cbu/hartleym/singularity"


def mkdir_parents(path):
    """Create the given directory path.

    This includes all necessary parent directories. Does not raise an error if
    the directory already exists.

    :param path: path to create
    """

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def create_software_paths(program_parameters):

    mkdir_parents(program_parameters['program_path'])


def generate_modulefile(program_parameters):
    return MODULEFILE_TEMPLATE.format(**program_parameters)


def create_modulefile(program_parameters):

    modulefile_contents = generate_modulefile(program_parameters)
    modulefile_dir = os.path.join(
        MODULEFILE_ROOT,
        program_parameters['program_name'])

    mkdir_parents(modulefile_dir)
    modulefile_file = os.path.join(
        modulefile_dir,
        program_parameters['program_version']) + '.lua'
    with open(modulefile_file, 'w') as fh:
        fh.write(modulefile_contents)


def move_singularity_image(program_parameters):
    from_path = os.path.join(
        SINGULARITY_ROOT,
        program_parameters['program_name'])

    to_path = os.path.join(
        program_parameters['program_path'],
        program_parameters['program_name'])

    # print("os.rename({}, {})".format(from_path, to_path))
    shutil.move(from_path, to_path)


def main():
    parser = argparse.ArgumentParser(__doc__)

    parser.add_argument(
        'program_name',
        help='Name of program and singularity image')
    parser.add_argument(
        'program_version',
        help='Version number of program')

    args = parser.parse_args()

    program_path = os.path.join(
        SOFTWARE_ROOT,
        args.program_name,
        args.program_version)

    program_parameters = dict(
        program_version=args.program_version,
        program_name=args.program_name,
        program_path=program_path)

    create_software_paths(program_parameters)
    create_modulefile(program_parameters)
    move_singularity_image(program_parameters)


if __name__ == '__main__':
    main()
