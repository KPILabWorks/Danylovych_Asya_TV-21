data= [(4,3), (6,2), (5,7), (7,1)]

# sorted() з lambda-функцією як ключом сортування
sorted_list = sorted(data, key = lambda x: x[1], reverse= True)

print(sorted_list)