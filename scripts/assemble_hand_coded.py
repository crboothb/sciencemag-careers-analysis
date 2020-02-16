import pickle
import pandas as pd

with open("pickles/hand_coded1.pickle", 'rb') as data:
    coded_df = pickle.load(data)
    # print(coded_df)


for i in range(1,10):
    # print("pickles/hand_coded"+str(i+1)+".pickle")
    with open("pickles/hand_coded"+str(i+1)+".pickle", 'rb') as data:
        new_df = pickle.load(data)
        coded_df = coded_df.append(new_df)
coded_df = coded_df.reset_index().drop(columns="index")

coded_df["input"] = coded_df["input"].astype(str)
indexNames = coded_df[ coded_df["input"] == "-" ].index
coded_df.drop(indexNames , inplace=True)
coded_df["input"] = coded_df["input"].astype(int)


print(coded_df.dtypes)
# print(len(coded_df))

# print(coded_df)