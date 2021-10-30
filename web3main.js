const Web3 = require('web3')

const netAddr = 'https://mainnet.infura.io/v3/d7af83af047d4230805fec39b32597af'
const provider = new Web3.providers.HttpProvider(netAddr)
const web3Inst = new Web3(provider)

const monitorAcc = '0x4dbe965abcb9ebc4c6e9d95aeb631e5b58e70d5b'.toLowerCase()

async function check(web3Instance) {
    let block = await web3Instance.eth.getBlock('latest')
    console.log(`Searching for block ${ block.number }...`)
    if (block && block.transactions) {
        for (let transactionHash of block.transactions) {
            let transaction = await web3Instance.eth.getTransaction(transactionHash)
            if (monitorAcc == transaction.to.toLowerCase()) {
                console.log({
                    address: transaction.from,
                    value: web3Instance.utils.fromWei(tx.value, 'ether'),
                    timestamp: new Date()
                })
            }
        }
    }
}


check(web3Inst)