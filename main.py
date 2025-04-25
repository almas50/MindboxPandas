import pandas as pd


def assign_sessions(df: pd.DataFrame) -> pd.DataFrame:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df = df.sort_values(['customer_id', 'timestamp'])

    df['time_diff'] = df.groupby('customer_id')['timestamp'].diff().dt.total_seconds() / 60

    df['is_new_session'] = (df['time_diff'] > 3).astype(int).fillna(0)

    df['session_id'] = df.groupby(['customer_id', 'is_new_session']).ngroup() + 1

    df.drop(columns=['time_diff', 'is_new_session'], inplace=True)

    return df


data = {
    'customer_id': [1, 1, 1, 2, 2],
    'product_id': [101, 102, 103, 201, 202],
    'timestamp': [
        '2024-04-25 10:00:00',
        '2024-04-25 10:01:30',
        '2024-04-25 10:05:00',
        '2024-04-25 09:00:00',
        '2024-04-25 09:02:00',
    ]
}

df = pd.DataFrame(data)
result = assign_sessions(df)
print(result)
