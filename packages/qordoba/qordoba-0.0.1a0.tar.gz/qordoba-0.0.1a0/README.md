# Q-CLI

[Build Status](http://jenkins)

[Documentation](https://dev.qordoba.com/docs/cli-dev)


## Introduction
With the Q-CLI we at Qordoba provide our customers an easy to use command line tool to push and pull files to our platform.
The package can also be executed to localize existing projects.
During the execution of the Q-CLI, technical but understandable output will be printed to the console. i18n output files will be written to the users desktop directory 'Output_Qordoba'.

#### Use-Cases:
1. You are a Qordoba customer and want to transfer files via the command line tool between your local machine and the Qordoba platform
2. You want to be a Qordoba customer and need to localize your app. Executing the Q-CLI i18n commands will help you localize your app. After the localization process has finished, contact our Sales Department for further on-boarding. <hello@qordoba.com>


## Installation
It is built for Python >= 2.7 for Mac OS X and Linux.

### from source
1. Download
2. Unpack
3. cd into directory
4. pip intstall .

### from [python package index](https://pypi.python.org/pypi/qordoba)
1. pip install qordoba


## Execution
- init
- pull
- push
- delete
- status
- ls
- find-new
- i18n-find
- i18n-rm
- i18n-mv


## Testing
 N/A - in progress

## Planned functionality
 N/A - in progress

## Versioning
Q-CLI adheres to Semantic Versioning 2.0.0. If there is a violation of this scheme, report it as a bug. Specifically, if a patch or minor version is
released and breaks backward compatibility, that version should be immediately yanked and/or a new version should be immediately released that restores
compatibility. Any change that breaks the public API will only be introduced at a major-version release. As a result of this policy, you can (and should)
specify any dependency on Q-CLI by using the Pessimistic Version Constraint with two digits of precision.

## Licensing
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Qordobacode/i18next-plugin/blob/master/LICENSE.md) file for details