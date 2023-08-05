[![][InfraBoxImage]][website]

# InfraBox CLI
[![Build Status](https://api.infrabox.net/v1/project/d4d0a859-d027-4a5a-8fc2-06495260f96a/build/state.svg)
](https://dashboard.infrabox.net/dashboard/project/d4d0a859-d027-4a5a-8fc2-06495260f96a)
[![coverage](https://api.infrabox.net/v1/project/d4d0a859-d027-4a5a-8fc2-06495260f96a/badge.svg?subject=coverage&job_name=pyinfrabox)](https://dashboard.infrabox.net/dashboard/project/d4d0a859-d027-4a5a-8fc2-06495260f96a)

## Install
To install infraboxcli you need to have these requirements already installed:

- git
- docker
- python & pip

Then simply run:

    pip install infraboxcli

You can validate your installation by running:

    infrabox version

## List Jobs
If you have a more complex project it may be helpful to list all available jobs in it. For this you may use:

    infrabox list

It outputs the names of all available jobs. An example output may look like this:

    tutorial-1
    tutorial-1/step1
    tutorial-1/step2
    tutorial-1/step3
    tutorial-1/step4
    tutorial-1/step5
    tutorial-1/tutorial-1/step1/tests
    tutorial-1/tutorial-1/step2/tests
    tutorial-1/tutorial-1/step3/tests
    tutorial-1/tutorial-1/step4/tests
    tutorial-1/tutorial-1/step5/tests

## Run a Job
InfraBox CLI may be used to run you jobs on your local machine. It will also respect all the dependencies and run the jobs in the correct order. Available options are:

    usage: infrabox run [-h] [--job-name JOB_NAME] [--clean] [-e ENVIRONMENT]

    optional arguments:
      -h, --help           show this help message and exit
      --job-name JOB_NAME  Job name to execute
      --clean              Runs 'docker-compose rm' before building
      -e ENVIRONMENT       Add environment variable to jobs

To run all jobs defined in your _infrabox.json_ file simply do:

    infrabox run


In case you have multiple jobs defined an want to run only one of them you can use the _--job-name_ option to specify which job you want to run.

    infrabox run --job-name <job-name>

Some of your job may require additional environment variables set from the outside. You can set as many environment varibles as you like with the _-e_ option.

    infrabox run -e VARNAME=SomeValue -e ANOTHERVAR=123

## Push a Job
To be able to use infrabox push you have to create a project in the InfraBox Dashboard first. See Create an upload project on how to create it. You also need the corresponding Project ID. See Get the ID of a project for instructions on how to obtain it. Last but not least a Access Token is required. See Create a Personal Access Token on how to setup one.

The Project ID and the Access Token must be set as environment variables.

    export INFRABOX_CLI_TOKEN=<YOUR_ACCESS_TOKEN>
    export INFRABOX_CLI_PROJECT_ID=<YOUR_PROJECT_ID>

To push your local project simply do:

    infrabox push

This will compress your local project and upload it to InfraBox. Now you can open the InfraBox Dashboard and navigate to your project. You should see the jobs running on InfraBox.

You can also watch the console output of your pushed jobs locally. Just use the _--show-console_ option.

    infrabox push --show-console

## Pull a Job
In case you would like to run a job which has been already executed on InfraBox you can use _infrabox pull_. It will download the docker container and all its inputs so you can the same container locally and investigate any issue.

    infrabox pull --job-id <JOB_ID>

You can find the exact command for each job on the job detail page of InfraBox under _Run local_

[InfraBoxImage]: https://infrabox.net/logo.png
[website]: https://infrabox.net


