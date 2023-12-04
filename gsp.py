import pandas as pd


#preprocessing
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

# Generate dataframe dictionary
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


all_frequent_itemsets = list()

min_support = float(input("Enter minimum support: "))
min_confidence = float(input("Enter minimum confidence: "))


def count_support(items):
    sup = 0
    for lst in df_dict:
        cnt = 0
        for str in df_dict[lst]:
            if items[cnt] in str:
                cnt += 1
                if cnt == len(items):
                    break
        if cnt == len(items):
            sup += 1
    return sup


# Generate frequent 1 itemsets
dist_item_set = set()
item_support_dict = dict()


def generate_distinct_items(df_dict):
    for lst in df_dict:

        for str in df_dict[lst]:

            for ch in str:
                dist_item_set.add(ch)


def generate_frequent_1_itemset(distinct_items):
    for item in distinct_items:
        cnt = 0
        for lst in df_dict:
            for str in df_dict[lst]:
                if item in str :
                    cnt += 1
                    break
        if cnt >= min_support:
            item_support_dict[item] = cnt


generate_distinct_items(df_dict)
dist_item_set = sorted(dist_item_set)  # convert set to sorted list
generate_frequent_1_itemset(dist_item_set)

if len(item_support_dict) != 0:
    all_frequent_itemsets.append(item_support_dict)

print(all_frequent_itemsets)

# Generate 2 frequent itemsets

if len(item_support_dict) > 1:
    frequent_2_itemset = dict()
    candidate_2_itemset = list()
    for key1 in item_support_dict.keys():

        for key2 in item_support_dict.keys():

            candidate_2_itemset.clear()
            candidate_2_itemset.append(key1)
            candidate_2_itemset.append(key2)
            count = count_support(candidate_2_itemset)

            if count >= min_support:
                frequent_2_itemset[tuple(candidate_2_itemset)]=count

            if key1 < key2:
                candidate_2_itemset.clear()
                item = key1 + key2
                candidate_2_itemset.append(item)
                count = count_support(candidate_2_itemset)

                if count >= min_support:
                    frequent_2_itemset[tuple(candidate_2_itemset)] = count

all_frequent_itemsets.append(frequent_2_itemset)


# Generate frequent itemsets bigger than 2

def can_join(items1, items2):
    cnt = 0
    for str in items2:
        if items1[cnt] in str:
            cnt += 1
            if cnt == len(items1):
                break
    if cnt == len(items1):
        return True
    else:
        return False


frequent_i_itemset = dict()

while len(all_frequent_itemsets[-1]) > 1:
    frequent_i_itemset.clear()
    last_set = all_frequent_itemsets[-1]

    for key1 in last_set.keys():
        for key2 in last_set.keys():
            if key1 == key2:
                continue
            else:
                temp1 = list(key1)
                temp2 = list(key2)

                if len(temp1[0]) == 1 and len(temp2[-1]) == 1:
                    temp1.pop(0)
                    temp2.pop()

                    if can_join(temp1,temp2):

                        k1 = list(key1)
                        k2 = list(key2)
                        k1.append(k2[-1])
                        cnt = count_support(k1)

                        if cnt >= min_support:
                            frequent_i_itemset[tuple(k1)] = cnt

                elif len(temp1[0]) == 1 and len(temp2[-1]) > 1:
                    temp1.pop(0)
                    temp2[-1] = temp2[-1][:-1]

                    if can_join(temp1, temp2):
                        k1 = list(key1)
                        k2 = list(key2)
                        k1[-1] += (k2[-1][-1])
                        cnt = count_support(k1)

                        if cnt >= min_support:
                            frequent_i_itemset[tuple(k1)] = cnt

                elif len(temp1[0]) > 1 and len(temp2[-1]) == 1:
                    temp1[0] = temp1[0][1:]
                    temp2.pop()

                    if can_join(temp1, temp2):
                        k1 = list(key1)
                        k2 = list(key2)
                        k1.append(k2[-1])
                        cnt = count_support(k1)

                        if cnt >= min_support:
                            frequent_i_itemset[tuple(k1)] = cnt

                elif len(temp1[0]) > 1 and len(temp2[-1]) > 1:
                    temp1[0] = temp1[0][1:]
                    temp2[-1] = temp2[-1][:-1]

                    if can_join(temp1, temp2):
                        k1 = list(key1)
                        k2 = list(key2)
                        k1[-1] += (k2[-1][-1])
                        cnt = count_support(k1)

                        if cnt >= min_support:
                            frequent_i_itemset[tuple(k1)] = cnt

    all_frequent_itemsets.append(dict(frequent_i_itemset))


def convert(list):
    str = ''
    for item in list:
        if len(item) == 1:
            str += item
        else:
            str += '('
            str += item
            str += ')'

    return str


frequents = list()

for dic in all_frequent_itemsets:
    for key in dic.keys():
        k = list(key)
        str = convert(k)
        frequents.append([str, dic[key]])


# Print all frequent itemsets
cnt = 1
for dic in all_frequent_itemsets :
    if len(dic) > 0:
        print('Frequent itemset of size', cnt, 'is   :')
        print(dic)
        print('\n')
        cnt += 1

print('______________________________________________________________________________\n')
print(frequents)


# STRONG RULES
def get_combinations(sequence):
    result = [[]]
    flag = True
    counter = 0
    for item in sequence:
        if item == ")":
            flag = True
            counter += 1
            continue
        if (not flag):
            counter += 1
            continue

        new_subsets = []

        if item == "(":
            flag = False
            nontemporal = ""
            for inneritem in sequence[counter:]:
                nontemporal += inneritem
                if inneritem == ")":
                    item = nontemporal
                    break

        for subset in result:
            if item not in subset:
                new_subsets.append(subset + [item])

        result.extend(new_subsets)

        counter += 1

    return result


def generate_association_rules(sequence):
    itemsets = get_combinations(sequence)

    association_rules = []
    # skip first and last index as they are empty set
    for element in itemsets[1:-1]:
        remaining = []
        flag = True

        counter = 0
        for item in sequence:
            if item == ")":
                flag = True
                counter += 1
                continue
            if not flag:
                counter += 1
                continue

            if item == "(":
                flag = False
                nontemporal = ""
                for inneritem in sequence[counter:]:
                    nontemporal += inneritem
                    if inneritem == ")":
                        item = nontemporal
                        break

            if item not in element:
                remaining.append(item)

            counter += 1

        rule = (element, remaining)

        association_rules.append(rule)

    return association_rules


def generate_strong_rules(association_rules, sequence, min_sup, min_conf):

    strong_rules = []

    for rule in association_rules:
        support = 0
        support_left = 0
        support_right = 0

        # support
        for item in frequents:

            mod_rule0 = ''.join(rule[0])
            mod_rule1 = ''.join(rule[1])

            if item[0] == sequence:
                support = item[1]

            if item[0] == mod_rule0:
                support_left = item[1]

            if item[0] == mod_rule1:
                support_right = item[1]

        if support == 0 or support_left == 0 or support_right == 0:
            continue
        # confidence
        confidence = support / support_left

        # lift
        lift = support / (support_right * support_left)

        if support >= min_sup and confidence >= min_conf:
            strong_rules.append(rule)
            print("Rule: ", rule)
            print("Support: ", support)
            print("Confidence: ", confidence)
            print("Lift = ", lift)

            if lift > 1:
                print("Rule is dependent and positively correlated\n")
            elif lift < 1:
                print("Rule is dependent and negatively correlated\n")
            else:
                print("Rule is independent\n")

    return strong_rules


print("\nAssociation rules: ")
for sequence in frequents:

    association_rules = generate_association_rules(sequence[0])
    for rule in association_rules:
        print(f"{rule[0]} -> {rule[1]}")

print("__________________________________")

print("\nStrong rules and their supprot/confidence/lift: ")
for sequence in frequents:
    strong_rules = generate_strong_rules(generate_association_rules(sequence[0]),sequence[0],min_support,min_confidence)
