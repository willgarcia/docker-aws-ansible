#!/bin/bash

set -eu

DOCKER_ENV_FILE=dockerenv

rm -f `pwd`/${DOCKER_ENV_FILE}
read -p "AWS local profile (see $HOME/.aws/credentials): " input; stty echo; echo AWS_MAIN_PROFILE=$input >> ${DOCKER_ENV_FILE}
read -p "AWS user name [eg: John.Doe]: " input; stty echo; echo AWS_MAIN_USER_ARN=${AWS_MAIN_USER_ARN}$input  >> ${DOCKER_ENV_FILE}
read -p "AWS MFA token (Google Auth, etc). 6-digits value: " input; stty echo; echo AWS_MAIN_MFA_TOKEN=$input >> ${DOCKER_ENV_FILE}
echo AWS_STS_ROLE_ARN=${AWS_STS_ROLE_ARN} >> ${DOCKER_ENV_FILE}
echo AWS_STS_PROFILE=${AWS_STS_PROFILE} >> ${DOCKER_ENV_FILE}
