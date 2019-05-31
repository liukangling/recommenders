# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
run_pytest.py is the script submitted to Azure ML that runs pytest.
pytest runs all tests in the specified test folder unless parameters
are set otherwise.
"""

import argparse
import subprocess

from azureml.core import Run


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Process inputs')
    # test folder
    parser.add_argument("--testfolder", "-f",
                        action="store",
                        default="./tests/unit",
                        help="Folder where tests are located")
    # internal test purposes
    parser.add_argument("--num",
                        action="store",
                        default="99",
                        help="test num")
    # test markers
    parser.add_argument("--testmarkers", "-m",
                        action="store",
                        default="not notebooks and not spark and not gpu",
                        help="Specify test markers for test selection")
    # test results file
    parser.add_argument("--xmlname", "-j",
                        action="store",
                        default="reports/test-unit.xml",
                        help="Test results")
    args = parser.parse_args()

    return(args)

if __name__ == "__main__":

    args = create_arg_parser()

    # run_pytest()

    print('junit_xml', args.xmlname)
    '''
    run_pytest(test_folder=args.testfolder,
               test_markers=args.testmarkers,
               junitxml=args.xmlname)
'''
    # Run.get_context() is needed to save context as pytest causes corruption
    # of env vars
    run = Run.get_context()
    '''
    This is an example of a working subprocess.run for a unit test run:
    subprocess.run(["pytest", "tests/unit",
                    "-m", "not notebooks and not spark and not gpu",
                    "--junitxml=reports/test-unit.xml"])
    '''
    print("args.junitxml", args.xmlname)
    print("junit=", "--junitxml="+args.xmlname)
    print('pytest run:',
          ["pytest",
           args.testfolder,
           "-m",
           args.test_markers,
           "--junitxml="+args.xmlname])
    subprocess.run(["pytest",
                    args.testfolder,
                    "-m",
                    args.testmarkers,
                    "--junitxml="+args.junitxml])
    # Leveraged code from this  notebook:
    # https://msdata.visualstudio.com/Vienna/_search?action=contents&text=upload_folder&type=code&lp=code-Project&filters=ProjectFilters%7BVienna%7DRepositoryFilters%7BAzureMlCli%7D&pageSize=25&sortOptions=%5B%7B%22field%22%3A%22relevance%22%2C%22sortOrder%22%3A%22desc%22%7D%5D&result=DefaultCollection%2FVienna%2FAzureMlCli%2FGBmaster%2F%2Fsrc%2Fazureml-core%2Fazureml%2Fcore%2Frun.py
    # print(("os.listdir files", os.listdir("."))
    # print(("os.listdir reports", os.listdir("./reports"))
    # print(("os.listdir outputs", os.listdir("./outputs"))

    #  files for AzureML
    name_of_upload = "reports"
    path_on_disk = "./reports"
    run.upload_folder(name_of_upload, path_on_disk)
