import pandas as pd
import time
def get_mae(df1,df2):
	mae = 0
	count = 0
	for index, row in df1.iterrows():
		for column in df1.columns[:-1]:
			if df1.iloc[index][column] != df2.iloc[index][column]:
				count+=1
				mae+= abs(df1.iloc[index][column] - df2.iloc[index][column])
	mae = mae / count if count else 0
	return mae
# Unconditional Mean Imputation
def get_unconditional_mean_imputation(file):
	complete = pd.read_csv('dataset_complete.csv', na_values=['?']) 
	data = pd.read_csv(file, na_values=['?']) 
	for column in data.columns[:-1]:
		mean = data[column].mean()
		#print("{} Mean : {}".format(column,mean))
		data[column].fillna(mean, inplace=True)

	return str(get_mae(data,complete))
 

# Hot Deck Imputation
def get_hot_deck_imputation(file):
	complete = pd.read_csv('dataset_complete.csv', nrows=5, na_values=['?']) 
	data = pd.read_csv(file, na_values=['?'], nrows=5 )
	closest_distances = {} 
	print(data)
	for index, row in enumerate(data.itertuples(), 0):
		closest_distances[index]= []
		print(index)
		for index2, row2 in enumerate(data.itertuples(), 0):
			if index == index2:
				continue
			distance =0
			count = 0
			for c in data.columns[:-1]:
				column = data.columns.get_loc(c)
				if not pd.isnull(row[column]) and not pd.isnull(row2[column]):
					distance+=abs(row[column]-row2[column])
					count+=1
			distance = distance / count if count else 0
			old_len = len(closest_distances[index])
			for index3, element in enumerate(closest_distances[index]):
				if element["distance"] < distance:
					closest_distances[index].insert(index3, {"row":row2, "distance":distance})
					break
			if len(closest_distances[index]) == old_len:
				closest_distances[index].append( {"row":row2, "distance":distance})
	for index, row in enumerate(data.itertuples(), 0):
		for ci, col in enumerate(data.columns[:-1]):
			if not pd.isnull(data.loc[index,col]):
				continue
			i = 0
			while pd.isnull(closest_distances[index][i]["row"][ci+1]):
				i+=1
			data.loc[index,col] = closest_distances[index][i]["row"][ci+1]
	print(data)
	# Get MAE
	return str(get_mae(data,complete))# # Conditional Mean Imputation

# Conditional Mean Imputation
def get_conditional_mean_imputation(file):
	complete = pd.read_csv('dataset_complete.csv', na_values=['?']) 
	data = pd.read_csv(file, na_values=['?']) 
	for column in data.columns[:-1]:
		no_mean = data[data["Binary Label"] == "No"][column].mean() 
		#print("{} No Mean : {}".format(column,no_mean))
		yes_mean = data[data["Binary Label"] == "Yes"][column].mean() 
		#print("{} Yes Mean : {}".format(column,yes_mean))
		data.loc[data["Binary Label"] == "No",column] = data.loc[data["Binary Label"] == "No",column].fillna(no_mean )
		data.loc[data["Binary Label"] == "Yes",column] = data.loc[data["Binary Label"] == "Yes",column].fillna(yes_mean )
	# Get MAE
	return str(get_mae(data,complete))# # Conditional Mean Imputation

# Conditional Hot Deck Imputation
def get_conditional_hot_deck_imputation(file):
	complete = pd.read_csv('dataset_complete.csv', nrows=5, na_values=['?']) 
	data = pd.read_csv(file, na_values=['?'], nrows=5 )
	closest_distances = {} 
	print(data)
	for index, row in enumerate(data.itertuples(), 0):
		closest_distances[index]= []
		print(index)
		for index2, row2 in enumerate(data.itertuples(), 0):
			if index == index2:
				continue
			distance =0
			count = 0
			for c in data.columns[:-1]:
				column = data.columns.get_loc(c)
				if not pd.isnull(row[column]) and not pd.isnull(row2[column]):
					distance+=abs(row[column]-row2[column])
					count+=1
			distance = distance / count if count else 0
			old_len = len(closest_distances[index])
			for index3, element in enumerate(closest_distances[index]):
				if element["distance"] < distance:
					closest_distances[index].insert(index3, {"row":row2, "distance":distance})
					break
			if len(closest_distances[index]) == old_len:
				closest_distances[index].append( {"row":row2, "distance":distance})
	for index, row in enumerate(data.itertuples(), 0):
		for ci, col in enumerate(data.columns[:-1]):
			if not pd.isnull(data.loc[index,col]):
				continue
			i = 0
			while i < len(closest_distances[index][i]) and (pd.isnull(closest_distances[index][i]["row"][ci+1]) or closest_distances[index][i]["row"][11]!= row[11]):
				i+=1
			if closest_distances[index][i]["row"][11]== row[11]:
				data.loc[index,col] = closest_distances[index][i]["row"][ci+1]
	print(data)
	# Get MAE
	return str(get_mae(data,complete))# # Conditional Mean Imputation
start = time.perf_counter()
# Main calls
#print("MAE_01_mean = {}".format(get_unconditional_mean_imputation('dataset_missing01.csv')))
#print("MAE_01_mean_conditional = {}".format(get_conditional_mean_imputation('dataset_missing01.csv')))
#print("MAE_01_hd = {}".format(get_hot_deck_imputation('dataset_missing01.csv')))
#print("MAE_01_hd_conditional = {}".format(get_conditional_hot_deck_imputation('dataset_missing01.csv')))
#print("MAE_20_mean = {}".format(get_unconditional_mean_imputation('dataset_missing20.csv')))
#print("MAE_20_mean_conditional = {}".format(get_conditional_mean_imputation('dataset_missing20.csv')))

print("MAE_20_hd = {}".format(get_hot_deck_imputation('dataset_missing20.csv')))
print("MAE_20_hd = {}".format(get_conditional_hot_deck_imputation('dataset_missing20.csv')))


end = time.perf_counter() - start

print("Time: "+str(end))
