# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


import os
import json
import argparse
import azureml.core
from azureml.core.authentication import AzureCliAuthentication
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE
# uncomment if using gpu
from azureml.core.runconfig import DEFAULT_GPU_IMAGE
from azureml.core.script_run_config import ScriptRunConfig


from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException


def submit_exp(testdir):
    with open("tests/ci/config.json") as f:
            config = json.load(f)

            workspace_name = config["workspace_name"]
            resource_group = config["resource_group"]
            subscription_id = config["subscription_id"]
            location = config["location"]

            print(" WS name ", workspace_name)
            print("subscription_id ", subscription_id)
            print("location", location)

            cli_auth = AzureCliAuthentication()
            print("cliauth")

    try:
        print("Trying to get ws")
        ws = Workspace.get(
            name=workspace_name,
            subscription_id=subscription_id,
            resource_group=resource_group,
            auth=cli_auth
        )

    except Exception:
        # this call might take a minute or two.
        print("Creating new workspace")
        ws = Workspace.create(
            name=ws,
            subscription_id=subscription_id,
            resource_group=resource_group,
            # create_resource_group=True,
            location=location,
            auth=cli_auth
        )

    # Choose a name for your CPU cluster
    cpu_cluster_name = "persistentcpu"
    # cpu_cluster_name = "cpucluster"
    print("cpu_cluster_name", cpu_cluster_name)
    # Verify that cluster does not exist already
    # https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-set-up-training-targets

    try:
        cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
        print('Found existing cluster, use it.')
    except ComputeTargetException:
        print("create cluster")
        compute_config = AmlCompute.provisioning_configuration(
                       vm_size='STANDARD_D2_V2',
                       max_nodes=4)
        cpu_cluster = ComputeTarget.create(ws,
                                           cpu_cluster_name,
                                           compute_config)

    cpu_cluster.wait_for_completion(show_output=True)

    # Create a new runconfig object
    # run_amlcompute = RunConfiguration(max_run_duration_seconds=60*30)
    run_amlcompute = RunConfiguration()

    # Use the cpu_cluster you created above.
    run_amlcompute.target = cpu_cluster

    # Enable Docker
    run_amlcompute.environment.docker.enabled = True

    # Set Docker base image to the default CPU-based image
    run_amlcompute.environment.docker.base_image = DEFAULT_CPU_IMAGE

    # Use conda_dependencies.yml to create a conda environment in the Docker image for execution
    run_amlcompute.environment.python.user_managed_dependencies = False

    # Auto-prepare the Docker image when used for execution (if it is not already prepared)
    run_amlcompute.auto_prepare_environment = True

    # Specify CondaDependencies obj, add necessary packages

    run_amlcompute.environment.python.conda_dependencies = CondaDependencies(
            conda_dependencies_file_path='./reco.yaml')

    experiment_name = 'PersistentAML'
'''
    experiment = Experiment(workspace=ws, name=experiment_name)
    project_folder = "."
    script_run_config = ScriptRunConfig(source_directory=project_folder,
                                        script='./tests/ci/runpytest.py',
                                        run_config=run_amlcompute)
'''
    print('testdir', testdir)
    script_run_config = ScriptRunConfig(source_directory=project_folder,
                                        script='testdir',
                                        run_config=run_amlcompute)

    print('before submit')
    run = experiment.submit(script_run_config)
    print('after submit')
    run.wait_for_completion(show_output=True, wait_post_processing=True)

    # go to azure portal to see log in azure ws and look for experiment name and
    # look for individual run
    print('files', run.get_file_names())
    run.download_files(prefix='reports')
    run.tag('persistentaml tag')


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
        This script generates a conda file for different environments.
        Plain python is the default, but flags can be used to support PySpark and GPU functionality"""
        ),
        epilog=HELP_MSG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--testdir",
                        action="store",
                        default="tests/unit/runpytest.py",
                        help="specify name of dir with tests")

    '''
    parser.add_argument("--name", help="specify name of conda environment")
    parser.add_argument(
        "--gpu", action="store_true", help="include packages for GPU support"
    )
    parser.add_argument(
        "--pyspark", action="store_true", help="include packages for PySpark support"
    )
    parser.add_argument(
        "--pyspark-version", help="provide specific version of PySpark to use"
    )
    args = parser.parse_args()

    # check pyspark version

    if args.pyspark_version is not None:
        args.pyspark = True
        pyspark_version_info = args.pyspark_version.split(".")
        if len(pyspark_version_info) != 3 or any(
            [not x.isdigit() for x in pyspark_version_info]
        ):
            raise TypeError(
                "PySpark version input must be valid numeric format (e.g. --pyspark-version=2.3.1)"
            )

    else:
        args.pyspark_version = "2.3.1"
    # overwrite environment name with user input
    if args.name is not None:
        conda_env = args.name

'''

    args = parser.parse_args()      
    submit_exp(args.testdir)