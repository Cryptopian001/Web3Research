# Web3Research

*We have the class `Address Monitor`*

1. Acquire an API key from https://etherscan.io/myapikey
2. Set up an Infura node at https://infura.io/
3. The idea is to retrieve the latest transactions of an account using the etherscan API, since we want to keep track of what we've been notified, use a `latest_block` variable to limit the block range to search
4. Obtain a URL to sent POST requests to a slack channel, reference video: https://www.youtube.com/watch?v=lEQ68HhpO4g&ab_channel=TechandBeyondWithMoss
5. build_slack_payload creates customized slack messages (in progress)

*Problems to be solved*
1. Figure out what coin each "to" address resolves to
2. Make slack messages more readable

sudo docker run -d --restart=always [container name]
