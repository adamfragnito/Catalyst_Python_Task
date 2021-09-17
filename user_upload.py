def load_csv(file):
    with open(file) as f:
        list_csv = f.readlines()
        #print(line)
        
        #list_csv.append(line)
    #print(list_csv)
    return list_csv

def read_csv(list_csv):
    headers = list_csv.pop(0)
    print("headers: ", headers)
    
    # str_csv = str(list_csv[0:1])
  #  print(str_csv)
    data = []
    for item in list_csv:
        #print(item)
        #data.append((item))
        first_name, surname, email = str(item).split(",")
        # print('firstname: ', first_name)
        # print('surname: ', surname)
        # print('email: ', email)
        data.append((first_name, surname, email))

    return data

file = "users.csv"
list_csv = load_csv(file)
# print(list_csv)
data = read_csv(list_csv)
print(data)

