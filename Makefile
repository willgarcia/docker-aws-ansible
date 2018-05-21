export AWS_STS_PROFILE=dev
export AWS_MAIN_USER_ARN=
export AWS_STS_ROLE_ARN=
export DOCKER_IMAGE=aws-ansible

.PHONY: check mfa-token run build

check:
	@which docker 2>&1 > /dev/null || (echo "No 'docker' on your PATH. Please, install it before proceeding." && exit 2)

mfa-token: check
	@sh build/dockerenv.sh

	@docker run \
		--volume $$HOME/.aws:/root/.aws \
		--interactive --tty \
		--env-file dockerenv \
		--entrypoint python \
		$$DOCKER_IMAGE /build/aws-credentials.py
	@echo "Configuration completed! Execute 'make run'."
	@echo "(Optional) If you have the AWS CLI installed, you can test your new AWS profile locally:"
	@echo "$$ export AWS_PROFILE=$(AWS_STS_PROFILE)"
	@echo "$$ aws cloudformation list-stacks --region ap-southeast-2"

run: check
	@docker run \
		--volume $$HOME/.aws:/root/.aws \
		--volume $$(pwd):/code \
		--interactive --tty \
		--entrypoint bash \
		$$DOCKER_IMAGE

build: check
	@docker rmi -f aws-ansible
	@docker build . -t aws-ansible:latest

