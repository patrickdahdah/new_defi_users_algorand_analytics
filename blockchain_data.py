
from algosdk.v2client import indexer
from algorand_defis import defi_mapping
from urllib import parse
import pandas as pd
import json
import requests


aex = "https://algoindexer.algoexplorerapi.io/"

# indexer_address = USE LOCALHOST PATH IF RUNNING THE NODE INDEXER, ELSE
# USE A PUBLIC API
indexer_address = aex
indexer_token = ''  # this field should be empty
indexer_client = indexer.IndexerClient(
    indexer_token=indexer_token,
    indexer_address=indexer_address)


COLUMNS = ['account', 'defi', "round", 'application_id', 'date']


def get_first_block_from_date(start_time: str) -> int:
    """get 1st block of a start time

    Args:
        start_time (str): any pandas datetime format

    Returns:
        int: block
    """
    # We need to format the time
    # indexer/api
    start_time_formatted = str(pd.to_datetime(start_time).isoformat()) + "Z"
    # use a endtime to avoid killing the indexer/api
    end_time_formatted = str(
        (pd.to_datetime(start_time) + pd.Timedelta(seconds=12)).isoformat()) + "Z"

    raw_data = indexer_client.search_transactions(
        start_time=start_time_formatted,
        end_time=end_time_formatted)

    return raw_data["transactions"][0]["confirmed-round"]


def get_defi_new_accounts(
        min_round: int, max_round: int) -> pd.DataFrame:
    """fetches transactions. filters in only the first
    interaction of an account with a certain defi application_id

    Args:
        min_round (int): Include results at or after the specified min-round.
        max_round (int): Include results at or before the specified max-round.

    Returns:
        DataFrame: appened rows with info for users first app interaction
    """

    assert(max_round >= min_round), "min block should be greater than max block"

    # current_round = -1
    current_round = min_round  # delete
    next_cursor = None
    final_df = pd.DataFrame(columns=COLUMNS)

    while max_round > current_round:
        print(" ")
        print("--fetching data--")
        print(current_round)
        if next_cursor is None:
            # USE THE FOLLOWING FUNCTION IF YOU ARE GETTING APIS FROM EXTERNAL
            # APIS:
            raw_data = get_transactions_from_public_api(
                {'min-round': min_round}, aex)
            # USE THE FOLLOWING FUNCTION IF YOU ARE RUNNING THE NODE INDEXER:
            # raw_data = indexer_client.search_transactions(
            #     min_round=min_round)
        else:
            # USE THE FOLLOWING FUNCTION IF YOU ARE GETTING APIS FROM EXTERNAL
            # APIS:
            raw_data = get_transactions_from_public_api(
                {'min-round': min_round, "next": next_cursor}, aex)
            # OR
            # USE THE FOLLOWING FUNCTION IF YOU ARE RUNNING THE NODE INDEXER:
            # raw_data = indexer_client.search_transactions(
            #     min_round=min_round, next_page=next_cursor)

        next_cursor = raw_data.get('next-token')

        # node always returns 'transactions' key, so no need to check for empty
        # blocks
        raw_transactions = raw_data['transactions']
        current_round = raw_transactions[-1]["confirmed-round"]
        print("number of transactions fetched => " + str(len(raw_transactions)))

        rows_df = get__defi_opt_ins(raw_transactions, defi_mapping)
        final_df = pd.concat([final_df, rows_df], axis=0)

    # avoid blocks out of ranges
    final_df = final_df[final_df["round"] <= max_round]

    return final_df


def get__defi_opt_ins(
        raw_transactions: dict,
        defi_mapping: dict) -> pd.DataFrame:
    """
    Ingest transactions to filter in only defi applications and opt-ins of users

    Args:
        raw_transactions (dict): raw transactions from the node indexer
        defi_mapping (dict): dict of application_id:defi_name

    Returns:
        pd.DataFrame: rows for info when users first app interaction
    """
    rows = []

    for transaction in raw_transactions:

        application_info = transaction.get('application-transaction')

        # checking if transaction is a smart-contract
        if application_info:
            # checking if is the first time the users is interacting with the
            # smart-contract ('optin' call)
            if application_info.get('on-completion') == 'optin':
                # map smart-contract with the fixed list of Defis
                application_id = application_info.get('application-id')

                # using dict key map for faster lookup
                defi_name = defi_mapping.get(application_id)
                if defi_name:

                    row = [
                        transaction.get('sender'),
                        defi_name,
                        transaction.get('confirmed-round'),
                        application_id,
                        transaction.get('round-time'),

                    ]

                    rows.append(row)

    rows_df = pd.DataFrame(rows, columns=COLUMNS)

    rows_df['date'] = pd.to_datetime(
        rows_df['date'], unit='s')
    return rows_df


def get_transactions_from_public_api(params, requrl):

    try:
        if params:
            requrl = requrl + "v2/transactions" + "?" + parse.urlencode(params)

        response = requests.get(
            requrl, timeout=20)

        response.raise_for_status()
        return json.loads(response.content)

    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
