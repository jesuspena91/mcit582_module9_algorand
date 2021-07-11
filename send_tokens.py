#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import account

#Connect to Algorand node maintained by PureStake
#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

# Generating an account
#account_private_key, account_address = account.generate_account()
account_private_key = 'BdzejpYMYzToTLMAPKajRYnLmxW+uDe+L6Gu7cUc1h3QsRxgnfx77NgbalH3/mvLuyoeZNu3f1WAs948BTV2+g=='
account_address = '2CYRYYE57R56ZWA3NJI7P7TLZO5SUHTE3O3X6VMAWPPDYBJVO35BE6G6NM'

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    tx = transaction.PaymentTxn(account_address, tx_fee, first_valid_round, 
        last_valid_round, gen_hash, receiver_pk, tx_amount, flat_fee=True)
    signed_tx = tx.sign(account_private_key)
    tx_confirm = acl.send_transaction(signed_tx)
    wait_for_confirmation(acl, txid=signed_tx.transaction.get_txid())

    return account_address, signed_tx.transaction.get_txid()

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo
