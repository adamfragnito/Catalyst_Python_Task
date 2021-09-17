import re
#import psycopg
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
    # print("headers: ", headers)
    data = []
    for item in list_csv:
        
        first_name, surname, email, email_valid = clean_items((item))
        if email_valid:
            data.append((first_name, surname, email))
        else:
            print(f'Email {email} is invalid - no insert will be made for user {first_name} {surname}')
    exit()

    return data



# def clean_items(first_name, surname, email):
def clean_items(item):
    #clean first name
    first_name, surname, email = str(item).split(",")
    
    first_name = first_name[0:1].upper() + first_name[1:].lower()
    
    regex = re.compile('[^a-zA-Z]+')
    first_name = regex.sub('', first_name)
    first_name = str(first_name).strip()
    print('first name cleaned is: ', first_name)

    #clean surname
    surname = surname[0:1].upper() + surname[1:].lower()     
    #check for apostraphe in surname and do not convert following letter to lowercase
    if "'" not in surname: 
        surname = surname[0:1].upper() + surname[1:].lower()
    else:
        surname = surname[0:1].upper() + "'" + surname[2:3].upper() + surname[3:].lower()

    surname = str(surname).strip()

    
    regex = re.compile("[A-Za-z0-9._'%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}") #regex to determine if valid email
    
    #validate emails : note on email regex : some web servers allow apostraphes so I have allowed it here  e.g. mo'connor@cat.net.nz is valied
    
    email_match = regex.match(email) or None #use match as it will match first one found, otherwise findall processes every email for every loop ???????
    #print(email_match.group(0))

    
    if (email_match is not None):
        #clean email
        email = email = email_match.group(0)
        email = email.lower()
        email = str(email).strip()
        print('cleaned email: ', email)
        print('email is valid: ', email)
        email_valid = True
    else:
        email_valid = False
        #invalid_emails.append(email)
    
    # print(invalid_emails)
    #email = regex.findall(email)
    return (first_name, surname, email, email_valid)


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
    
    parser.add_argument('--create_table', action='store_true', help=help_message)

    help_message = """
    --dry_run – this will be used with the --file directive in case we want to run the script but not
        insert into the DB. All other functions will be executed, but the database won't be altered
    """
    parser.add_argument('--dry_run', action='store_true', help=help_message)

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


def create_postgres_table(data, args):
    dbname = "PostgreSQL" #assumed, no directive given for this in specs, same with port number
    username = args.username
    print("username ",  username)
    passwd = args.password
    print("password ",  passwd)
    host = args.host
    print("username ",  username)

    #make db connection
    # conn = psycopg2.connect(database=dbname, user=username, password=passwd, host=host) #, port= ) no port given
    #create table with data
    # cursor = conn.cursor()
    sql = "CREATE TABLE users(name varchar2(25) NOT NULL, surname varchar2(50) NOT NULL, email NOT NULL UNIQUE)"
    
    print(sql)
    # cursor.execute(sql)
    for item in data:
        name = item[0]
        surname = item[1]
        email = item[2]
        #sql =  "INSERT INTO users(name, surname, email) VALUES(" + item[0] + "," + item[1] + "," + item[2] + ""
        sql = ("""INSERT INTO users(name, surname, email) VALUES(%s, %s, %s)""",(name, surname, email))
        print(sql)
    # conn.commit


def process_command_line_args(args):
    #if args.file in argv:
    print('dry run ', args.dry_run)
    
    print(args.file)
    if args.file is not None:
        csv_file = args.file
        list_csv = load_csv(csv_file)
        data = read_csv(list_csv)

    print(args.create_table)
    print('print data ', data)
    if len(data) > 0 and args.dry_run is False:
        create_postgres_table(data, args)
        #csv_file = args.table
        #create postgres table
    else:
       print("data is ", data) 

def main():
    args = create_command_line_args()
    process_command_line_args(args)

    #print(argv)
    #process_arguements
            
    
    #print(args.file)
    #print(args.table)
    #print(args.dry_run)
    #print(args.username)
    #print(args.password)
    #print(args.host)
      
    

# if __name__ != "__main__":
main()



