import re
#import psycopg
import sys
from argparse import ArgumentParser
#from config import config


#from validate_email import validate_email

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

        clean_items(first_name, surname, email)
        data.append((first_name, surname, email))

    print(data)
    return data



def clean_items(first_name, surname, email):
    #for index, item in enumerate(data):
    first_name = first_name[0:1].upper() + first_name[1:].lower()

    surname = surname[0:1].upper() + surname[1:].lower()     

    regex = re.compile('[^a-zA-Z]+')
    first_name = regex.sub('', first_name)
    print('first name cleaned is: ', first_name)

    #check for apostraphe in surname and do not convert following letter to lowercase
    if "'" not in surname: 
        surname = surname[0:1].upper() + surname[1:].lower()
    else:
        surname = surname[0:1].upper() + "'" + surname[2:3].upper() + surname[3:].lower()

    print('surname cleaned is: ', surname)

    # validate email later  -   use validate email package

    email = str(email).strip("\n")
    print('email stripped: ', email)
    regex = re.compile('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}')
    emails = regex.findall(email)
    print("valid emails: ", emails)
    # print('firstname: ', first_name)
    # print('surname: ', surname)
    # print('email: ', email)
    # email = data[0][index]

def create_postgres_table():
    pass

def create_command_line_args():

    parser = ArgumentParser()
    #parser.add_argument("--file", "pos_arg_1", help="--file [csv file name] – this is the name of the CSV to be parsed")
    # parser.add_argument("-q", "--quiet",
    #                     action="store_false", dest="verbose", default=True,
    #                     help="don't print status messages to stdout")
    help_message = """
    --file [csv file name] – this is the name of the CSV to be parsed\n
    """
    #parser.add_argument('--help', dest='help')#, help=help_message)
    
    parser.add_argument('--file', dest='file', help=help_message)
    help_message = """
    --create_table – this will cause the PostgreSQL users table to be built (and no further action
      will be taken)
    """
    
    parser.add_argument('--create_table', dest='table', help=help_message)

    help_message = """
    --dry_run – this will be used with the --file directive in case we want to run the script but not
        insert into the DB. All other functions will be executed, but the database won't be altered
    """
    parser.add_argument('--dry_run', dest="dry_run", help=help_message)

    help_message = """
    -u – PostgreSQL username
    """
    parser.add_argument('-u', dest="username", help=help_message)

    help_message = """
    -p – PostgreSQL password
    """
    parser.add_argument('-p', dest="password", help=help_message)

    help_message = """
    -h – PostgreSQL host
    """
    parser.add_argument('-host', dest="host", help=help_message)

    args = parser.parse_args()
    return args
        # if "--file" in args:
        #     print('found file arg')


#print(data)
#clean_items(data)

def main(argv):
    args = create_command_line_args()
    print(args.file)
    print(args.table)
    print(args.table)
    print(args.dry_run)
    print(args.username)
    print(args.password)
    print(args.host)
      
    csv_file = args.file
    list_csv = load_csv(csv_file)
    data = read_csv(list_csv)

# if __name__ != "__main__":
main(sys.argv)



