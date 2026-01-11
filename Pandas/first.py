import pandas as pd

# data=[100,101,204,103,102,205,206]
# series=pd.Series(data, index=["a","b","c","d","e","f","g"])
# # print(series)
# print(series[series<200])

# calories = {"Day 1":1750,"Day 2":2100, "Day 3":2200, "Day 4":2300}
# series = pd.Series(calories)
# print(series)

# data={
#     "Name": ["Eevee", "Lucario", "Gardevoir"],
#     "Level": [15,23,36]
# }
# # data_frame = pd.DataFrame(data)
# # print(data_frame)
# data_frame=pd.DataFrame(data, index=["Pokemon 1", "Pokemon 2", "Pokemon 3"])
# # print(data_frame)
# data_frame["HP"]=[100, 95, 76]
# # print(data_frame)
# new_row=pd.DataFrame([{"Name": "Absol", "Level":17,"HP":90}], index=["Pokemon 4"])
# df=pd.concat([data_frame,new_row])
# print(df)

df=pd.read_csv("test.csv")
# # print(df)
# print(df.to_string())
# df=pd.read_json("data.json")
# print(df)

print(df["Name"].to_string( ))


