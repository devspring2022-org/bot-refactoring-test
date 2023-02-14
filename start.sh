docker rm -f pr-automation
docker run -d --network=host --restart always --name pr-automation -e RUNNER_NAME="pr-automation" -e RUNNER_GROUP="bot" -e ACCESS_TOKEN="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" -e RUNNER_SCOPE="org" -e ORG_NAME="devspring2022-org" -e PR_BOT_CONFIG_PATH="D:\Templates\config" -v /var/run/docker.sock:/var/run/docker.sock myoung34/github-runner:latest
