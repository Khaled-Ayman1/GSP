import pandas as pd


def preprocessing(df):

    # remove whitespaces from string columns
    for col in df.columns:
        col = col.strip()
        if df[col].dtype == 'object':  # check if the column contains strings
            df[col] = df[col].str.strip()

    # drop null
    df.dropna(how='any', inplace=True)

    df.reset_index(drop=True, inplace=True)


test_df = pd.read_excel('data/test_data.xlsx')

preprocessing(test_df)


df_dict = {}

for index in range(len(test_df)):

    non_temporal = ''
    flag = False
    itemlist = list(test_df.iloc[index, 1])
    insert_index = 0
    item_index = 0

    while item_index < len(itemlist):

        item = itemlist[item_index]

        if item == '(':
            insert_index = item_index
            flag = True
            item = ''

        elif item == ')':
            flag = False
            item = ''

            for i in range(insert_index, item_index + 1):
                itemlist.pop(insert_index)

            itemlist.insert(insert_index,non_temporal)
            non_temporal = ''
            item_index = insert_index

        elif flag:
            non_temporal += item
            item = ''

        item_index += 1

    df_dict[test_df.iloc[index, 0]] = itemlist

print(df_dict)
