import pandas as pd
import glob
import datetime

last_data = []
keyword = ['게임', 'GAME', '뉴스', 'NEWS', '음악', 'MUSIC', '요리', 'COOK', '애완동물', 'PETS', '스포츠', 'SPORTS']
for i in keyword:
    data_paths = glob.glob('./data/data_{}_*'.format(i))
    if data_paths:
        last_data.append(data_paths[-1])

print(last_data)

df = pd.DataFrame()
for path in last_data:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df = pd.concat([df, df_temp])

if not df.empty:
    # Check if 'keyword' column is present in the DataFrame
    if 'keyword' in df.columns:
        print(df['keyword'].value_counts())
    else:
        print("Column 'keyword' not found in the DataFrame.")

    df.info()

    df.to_csv('./Youtube_titles_{}.csv'.format(
        datetime.datetime.now().strftime('%Y%m%d')), index=False)
else:
    print("DataFrame is empty. No CSV file generated.")