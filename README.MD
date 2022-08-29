#  | On-Chain Data Challenge | 

## WILD CARD OPTION✨

For the On-chain Data task, I have decided to build a behavior analytics script for Algorand's new Defi users.
Behavioral analytics allows you to determine exactly how your users interact with the products.
With this data, companies and communities can see exactly how users interacted between different digital experiences of the blockchains' dapps. Make all types of decisions like investments, evaluating blockchain users, where to build DAOs, which blockchain to choose for a dapp, etc...

A deep understanding of user behavior is necessary to move all of core metrics, whether it’s retention, lifetime value, conversion rate, or revenue. **I belive there is no sufficient offerings for behavioral data in the blockchain industry and it should be taken into account given how insightful this type of metrics are. Which is why i choosed this On-Chain Data Challenge topic**
I choose Algorand because it is a network i have experience with and is one with no Defi winner, meaning that users are spread out in different defis

### Data Source:

To comply with the Challenge instructions, I fetched the transactions from the [Algorand node indexer](https://developer.algorand.org/docs/run-a-node/setup/indexer/) (Algorand doesnt have an sdk or an intuitive way to get transaction batches [directly from node](https://developer.algorand.org/docs/rest-apis/algod/v2/)). Since my laptop doesnt meet the [hardware storage requirments](https://developer.algoscan.app/) to run a full node_indexer, I used an open api that is compatible with the node indexer [api calls](https://developer.algorand.org/docs/rest-apis/indexer/).

python sdk ([py-algorand-sdk](https://py-algorand-sdk.readthedocs.io/en/latest/)) to fetch from node indexer/compatible apis: https://developer.algorand.org/docs/sdks/python/

i could have used the (algoexplorer enriched indexer)[https://indexer.algoexplorerapi.io/swagger.json] which has normalized and richer data but i wanted to stick with the tasks challenges and makes sense since not all blockchains have a free enriched api

> The code will run with a preloaded june_and_july.csv data
> To run the code with no preloaded data just comment the line 21-23 and uncomment line 19 from main.py

### Which Defis we will be tracking?

List was based on defi's with a relatively high amount of Twitter followers and if their assets are verified:

- ['Tinyman' 31k](https://tinyman.org/)
- ['Algofi' 23.7k](https://algofi.org/)
- ['HumbleSwap' 6.6k](https://app.humble.sh/pool)
- ['Folks' 10.9k](https://folks.finance/)

'AlgoDEX' was left out since i noticed a very big number of artificial created accounts intercating with the defi with no buys and sells ever created

## Explanation

### 1 Get Defi_name<>application_ids

On Algorand, Defis consists of multiple application_ids interacting with accounts. This means that there are several application_ids per Defi App. The number of applications_id per defi varies between their implementation, so we need to map the application_ids with their respective defi to link accounts with defi names. We do this programmatically by extracting the API from the frontend that the algoexplorer uses in their application website (https://algoexplorer.io/applications).
We create a dictionary with the application_ids:defi_name in the algorand_defi.py that we will use to map the transactions with the list of defi applications.

### 2 Get first account interactions with the defi

In this Challenge, we only care about transactions that are interacting with the application as "Opt-ins", which are the first interaction of users with the application_id

### 3 Extract and Return Defi data

We digest the transactions and return the data as a Dataframe to the main file where we will be building the insights using pandas.

## Prerequisites

```bash
pip install pandas py-algorand-sdk matplotlib
```

no need to run the node indexer, the code will be using a public api which connects to a node indexer.
to change this simply comment the `get_transactions_from_public_api` function and use the function of the `indexer_client`

## Run the script

> The code will run with a preloaded june_and_july.csv data
> To run the code with no preloaded data just comment the line 21-23 and uncomment line 19 from main.py

```bash
python main.py
```

# Results

## 1. High Engagement Users

list and count of defi accounts,
list and count of highly engaged defi accounts (intercated with more than 2,3 defis)

Percentage of defi accounts with more than one defi interaction

- Ideal list of accounts for airdrops

## 2. Growth of new defi users on Algorand

line chart plot

## 3. Proportion of participating accounts per defi

Pie chart

## 4. Daily New Accounts per Defi

Stacked Area line chart for better visualization of trend changes

## 5. Timezone of Algorand Defi Users

Example: The most active hours are from 16:00 UTC till 20:00 UTC

## 6. Median time between the first interaction of two different defis

Example: 8 days is the median time for engaged users to try out two different defis

# Contact

**Please reach out if you have any questions, this might be very confusing.**
