from web3 import Web3
import tweepy
import json

# Web3 and contract configuration
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
CONTRACT_ADDRESS = "0xYourContractAddress"
PRIVATE_KEY = "YourPrivateKey"
ACCOUNT_ADDRESS = "YourWalletAddress"
ABI = json.loads('''[Your Contract ABI Here]''')  # Replace with actual ABI

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Twitter API configuration
API_KEY = "YourTwitterAPIKey"
API_SECRET = "YourTwitterAPISecret"
ACCESS_TOKEN = "YourAccessToken"
ACCESS_SECRET = "YourAccessSecret"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Function to scrape tweets
def scrape_tweets(query, count=10):
    tweets = api.search_tweets(q=query, count=count, lang="en")
    flagged_wallets = []
    for tweet in tweets:
        if "0x" in tweet.text:  # Simplistic wallet detection
            flagged_wallets.append(tweet.text.split("0x")[1][:42])
    return flagged_wallets

# Function to flag wallet
def flag_wallet(wallet, reason):
    nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
    txn = contract.functions.flagAddress(wallet, reason).build_transaction({
        'chainId': 1,
        'gas': 200000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': nonce
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash.hex()

# Main process
if __name__ == "__main__":
    query = "scam alert"
    wallets = scrape_tweets(query)
    for wallet in wallets:
        try:
            tx_hash = flag_wallet(wallet, "Flagged by Oxint bot")
            print(f"Flagged {wallet}. TX: {tx_hash}")
        except Exception as e:
            print(f"Error flagging {wallet}: {str(e)}")
