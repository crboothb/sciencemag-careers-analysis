import pickle
import pandas as pd

with open("pickles/hand_coded1.pickle", "rb") as data:
    coded_df = pickle.load(data)
    # print(coded_df)
with open("pickles/hand_coded1_2.pickle", "rb") as data:
    new_df = pickle.load(data)
    coded_df = coded_df.append(new_df)

for i in range(1, 10):
    # print("pickles/hand_coded"+str(i+1)+".pickle")
    print(i+1)
    with open("pickles/hand_coded" + str(i + 1) + ".pickle", "rb") as data:
        new_df = pickle.load(data)
        coded_df = coded_df.append(new_df)
        # print(len(coded_df))
    with open("pickles/hand_coded" + str(i + 1) + "_2.pickle", "rb") as data:
        new_df = pickle.load(data)
        coded_df = coded_df.append(new_df)
        # print(len(coded_df))
coded_df = coded_df.reset_index().drop(columns="index")

coded_df["input"] = coded_df["input"].astype(str)
indexNames = coded_df[coded_df["input"] == "-"].index
coded_df.drop(indexNames, inplace=True)
coded_df["input"] = coded_df["input"].astype(int)

with open("pickles/hand_coded_ALL.pickle", "wb") as output:
    pickle.dump(coded_df, output)

print("done")

# print(coded_df.dtypes)
# print(len(coded_df))

# print(coded_df)
