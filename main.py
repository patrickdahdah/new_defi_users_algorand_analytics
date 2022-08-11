import pandas as pd
import matplotlib.pyplot as plt
import time
from blockchain_data import get_defi_new_accounts, get_first_block_from_date

start_time = '2022-06-01T00:00:00'
end_time = '2022-07-01T00:00:00'
print("HODL")

# # getting block ranges, the node doesnt accept timestamps
# first_block = get_first_block_from_date(start_time)
# time.sleep(0.1)
# last_block = get_first_block_from_date(end_time) - 1


# COLUMNS = ['account', 'defi', "round", 'application_id', 'date']
# USE THIS FUNCTION IF YOU HAVE DEPLOYED THE NODE INDEXER OR USING PUBLIC APIS
# defi_transactions = get_defi_new_accounts(first_block, last_block)

# USE THIS FUNCTION FROM LOCAL FILE IF YOU HAVE THE CSV
defi_transactions = pd.read_csv("june_and_july.csv")
defi_transactions['date'] = pd.to_datetime(
    defi_transactions['date'])


# getting number of users and number of distincts defis per user
users_unique_defis = defi_transactions.groupby("account")[
    "defi"].nunique()


# 1. High Engagement Users
print("\n-- 1. High Engagement Users    --")
active_addresses = users_unique_defis[users_unique_defis.gt(1)]
very_active_addresses = users_unique_defis[users_unique_defis.gt(2)]

users_unique_defis_count = len(users_unique_defis.index)
active_addresses_count = active_addresses.count()
very_active_addresses_count = very_active_addresses.count()
print("Number of defi Accounts: {}\n\
Accounts that have tried out two or more different defis: {}\n\
Accounts that have tried out three or more different defis: {}\n".format(users_unique_defis_count, active_addresses_count, very_active_addresses_count))

# 1.1 Percentage of High Engagement Users
print("\n       --  1.1 High Engagement Users   --")
percentage_of_active_addresses = (
    active_addresses_count / users_unique_defis_count) * 100
percentage_of_very_active_addresses = (
    very_active_addresses_count / users_unique_defis_count) * 100

print("percentage of active users: ", format(
    percentage_of_active_addresses, ".3f"), "%")

print("percentage of very active users: ", format(
    percentage_of_very_active_addresses, ".3f"), "%")


# 2 New Defi Accounts on Algorand
print("\n--2. New Defi Accounts on Algorand --")

df_new_defi_accounts_daily = defi_transactions.groupby(
    pd.Grouper(key='date', freq='D'))["account"].nunique()

df_new_defi_accounts_daily.plot(title="2. New Defi Accounts on Algorand")
plt.show()

# 3. Proportion of participating accounts per defi
print("\n--3. Proportion of participating accounts per defi --")
df_count_per_defi = defi_transactions[['account', 'defi']].groupby(
    'defi').nunique()

print(df_count_per_defi.head(5))

df_count_per_defi.plot(

    kind='pie',

    y='account',
    figsize=(
        5,
        5),

    autopct='%1.1f%%',

    startangle=90,
    title='3. Proportion of participating accounts per defi')
plt.show()

# 4.  Daily New Accounts per Defi
print("\n--4.  Daily New Accounts per Defi --")
# Grouping by accounts and defi to get first time a user intercated with
# each  defi
df_account_defi = defi_transactions[['account', 'defi', 'date']].groupby(
    ['account', 'defi']).min().reset_index()


df_stacked_bar_chart = df_account_defi.groupby(
    [pd.Grouper(key='date', freq='D'), 'defi']).count()

plt.show()


df_stacked_bar_chart.pivot_table(
    index='date',
    columns='defi',
    values='account').plot(
        kind='area',
    title='4.1 |Area|Daily New Accounts per Defi')

plt.show()


# 5.  Timezone of Algorand Defi Users
print("\n--5. Timezone of Algorand Defi Users --")

# trunc date to get hours
defi_transactions['hour'] = defi_transactions['date'].dt.hour

# get most active hours, sorted descending method
top_hours_activity = defi_transactions.groupby(
    "hour")["account"].nunique().sort_values(ascending=False).head(4)

print("The most active hours are from {}:00 UTC till {}:00 UTC".format(
    top_hours_activity.index[0], top_hours_activity.index[-1] + 1))

# 6.  Median time between the first interaction of two different defis
print("\n--6.  Median time between the first interaction of two different defis --")
engaged_users = users_unique_defis[users_unique_defis.eq(2)].index


df_transactions_engaged_users = defi_transactions[defi_transactions['account'].isin(
    engaged_users)]

df_start_times = df_transactions_engaged_users.groupby(
    ['account', 'defi'])['date'].min().reset_index().sort_values('date')

df_time_diffs = df_start_times.groupby('account')['date'].diff()

median_interaction_time = df_time_diffs.median()
print("Median time between the first interaction of two different defis is {}".format(
    median_interaction_time))
