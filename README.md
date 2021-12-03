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

Dec, 3, 2021
1. Solved address to coin name resolution problem
2. Made slack messages more readable

*Problems to be solved*
1. Not all addresses can be resolved to a coin name, find out ways to do so, a potential solution would be to find more sources, and write a function to merge the address-to-coin-name mapping from different sources when initializing the program
2. Sometimes connection with the web3 API becomes unstable, resulting in a "reached max connect retries" problem, which restarts the container, we might miss on transactions during the delay
3. It is very hard to write unit tests for the program, finding out a way to do tests would be helpful

No other problems have been observed as of right now, need to continue monitoring the program
