# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
run_pytest.py is the script submitted to Azure ML that runs pytest.
pytest runs all tests in the specified test folder unless parameters
are set otherwise.
"""

import os
import argparse
import subprocess

from azureml.core import Run


def create_arg_parser():

    parser = argparse.ArgumentParser(description='Process inputs')
    parser.add_argument("--testfolder",
                        action="store",
                        default="./tests/unit",
                        help="folder where tests are located")
    parser.add_argument("--num",
                        action="store",
                        default="99",
                        help="test num")
    parser.add_argument("--markers",
                        action="store",
                        default="not notebooks and not spark and not gpu",
                        help="Specify test markers for test selection")
    parser.add_argument("--junitxml",
                        action="store",
                        default="--junitxml=reports/test-unit.xml",
                        help="Test results")

    args = parser.parse_args()
    return(args)


def run_pytest(test_folder="./tests/unit",
               test_markers="not notebooks and not spark and not gpu",
               junitxml="--junitxml=reports/test-unit.xml",
               test_num="77"):
    '''
    This is the script that is submitted to AzureML to run pytest.

    Args:
         test_folder  (str): folder that contains the tests that pytest runs
         test_markers (str): test markers used by pytest "not notebooks and
                             not spark and not gpu"
         junitxml     (str): file of output summary of tests run
                             note "--junitxml" is required as part of
                             the string
                             Example: "--junitxml=reports/test-unit.xml"
    Return: none

    print('run_py: before run.get_context')
    # Run.get_context() is needed to save context as pytest causes corruption
    # of env vars
    run = Run.get_context()
    print('run_py: before subprocess.run')
    '''
    # Run.get_context() is needed to save context as pytest causes corruption
    # of env vars
    run = Run.get_context()
    '''
    subprocess.run(["pytest", "tests/unit",
                    "-m", "not notebooks and not spark and not gpu",
                    "--junitxml=reports/test-unit.xml"])
    '''
    # run_time = time.time - start_time

    '''
    # run.log(name='Test Run', value='Unit Test Staging')
    '''
    print('run_py: test_folder:%s, test_markers:%s, junitxml:%s' %
          (test_folder, test_markers, junitxml))
    print('list:', ["pytest", test_folder, "-m", test_markers, junitxml])
    subprocess.run(["pytest", test_folder, "-m", test_markers, junitxml])
    print("os.listdir files", os.listdir("."))
    print("os.listdir reports", os.listdir("reports"))
    print("os.listdir reports", os.listdir("outputs"))

    # set up reports
    name_of_upload = "reports"
    path_on_disk = "./reports"
    run.upload_folder(name_of_upload, path_on_disk)
    run.upload_file("reports", "./reports/test-unit.xml")
    # next try
    # run = experiment.start_logging()
    # run.upload_folder(name='important_files', path='path/on/disk')
    # run.download_file('important_files/existing_file.txt', 'local_file.txt')
    # code here:
    # https://msdata.visualstudio.com/Vienna/_search?action=contents&text=upload_folder&type=code&lp=code-Project&filters=ProjectFilters%7BVienna%7DRepositoryFilters%7BAzureMlCli%7D&pageSize=25&sortOptions=%5B%7B%22field%22%3A%22relevance%22%2C%22sortOrder%22%3A%22desc%22%7D%5D&result=DefaultCollection%2FVienna%2FAzureMlCli%2FGBmaster%2F%2Fsrc%2Fazureml-core%2Fazureml%2Fcore%2Frun.py


if __name__ == "__main__":

    args = create_arg_parser()
    print("arg.num ", args.num)
    # run_pytest()
    '''
    run_pytest(test_folder=args.testfolder,
               test_markers=args.markers,
               junitxml=args.junitxml)
    '''
    run_pytest(test_folder=args.testfolder,
               test_markers=args.markers,
               junitxml="--junitxml="+args.markers,
               test_num=args.num)
