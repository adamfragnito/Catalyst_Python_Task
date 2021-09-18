import re
import psycopg2

from psycopg2 import sql
from argparse import ArgumentParser
#from config import config

#from validate_email import validate_email

def load_csv(file):
    """
    open file and read the contents into a list
    params: csv file
    """

    with open(file) as f:
        list_csv = f.readlines()
        
    return list_csv

def process_csv(list_csv):
    """
    extract data from csv file into workable format, call clean routine beforehand
    params: csv list
    """
    headers = list_csv.pop(0) # extract headers i.e. name,surname,email
    
    data = []
    for item in list_csv:
        first_name, surname, email, email_valid = clean_items((item))
        if email_valid:
            data.append((first_name, surname, email)) #append data only if email is valid
        else:
            print(f'Email {email} is invalid - no insert will be made for user {first_name} {surname} \n')

    return data


def clean_items(item):
    """
    cleans items into appropriate format
    params: item - a row of data
    """
    
    #clean first name
    first_name, surname, email = str(item).split(",")
    
    first_name = first_name[0:1].upper() + first_name[1:].lower()
    
    regex = re.compile('[^a-zA-Z]+')
    first_name = regex.sub('', first_name)
    first_name = str(first_name).strip()
    
    #clean surname
    surname = surname[0:1].upper() + surname[1:].lower()     
    #check for apostraphe in surname and do not convert following letter to lowercase
    if "'" not in surname: 
        surname = surname[0:1].upper() + surname[1:].lower()
    else:
        surname = surname[0:1].upper() + "'" + surname[2:3].upper() + surname[3:].lower()

    surname = str(surname).strip()

    #define regular expression for valid email format
    #note : some web servers allow apostraphes so I have allowed it here  e.g. mo'connor@cat.net.nz is valid
    regex = re.compile("[A-Za-z0-9._'%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")
    
    #match on valid emails
    email_match = regex.match(email) or None
    
    if (email_match is not None):
        #clean email if valid
        email = email = email_match.group(0)
        email = email.lower()
        email = str(email).strip()
        email_valid = True
    else:
        #invalid email
        email_valid = False
    
    return (first_name, surname, email, email_valid)


def create_command_line_args():
    """
    build the command line arguments using argparse module
    params: none
    """

    parser = ArgumentParser()
    
    #define help text for each command line argument and add argument to parser
    help_message = """
    --file [csv file name] – this is the name of the CSV to be parsed\n
    """
    
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

    # define host option as -host, not -h as this will conflict with the build in switches for help i.e. -h, --help
    help_message = """
    -host – PostgreSQL host
    """
    parser.add_argument('-host', dest="host", help=help_message)

    args = parser.parse_args()
    return args


def create_postgres_table(data, args):
    """
    create db table and insert data
    param:  data - cleaned data ready for insert
            args - command line arguments entered by user
    """

    #define db parameters
    dbname = "postgres" #assumed, no directive given for this in specs, same with port number
    username = args.username
    passwd = args.password
    host = args.host
    
    #make db connection
    conn = psycopg2.connect(database=dbname, user=username, password=passwd, host=host) #, port= ) no port given
    #define cursor object
    cursor = conn.cursor()
    #build query
    query_str = "CREATE TABLE IF NOT EXISTS users(name varchar(25) NOT NULL, surname varchar(50) NOT NULL, email varchar(50) UNIQUE NOT NULL)"
    query = sql.SQL(query_str)

    #execute and commit query
    cursor.execute(query)
    conn.commit()
    
    for item in data:
        #extract values from data
        name_val = item[0]
        surname_val = item[1]
        email_val = item[2]
        
        #insert into db
        try:
            cursor.execute('INSERT INTO users (name, surname, email) VALUES (%s, %s, %s)', (name_val, surname_val, email_val))
        #rollback transaction if duplicate email is found and move on
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            continue
        except psycopg2.errors.InFailedSqlTransaction as e:
            print('Insert aborted: ', e)
            continue
        else:
            conn.commit()
            print('row written to database')


def process_command_line_args(args):
    """
    processes the command line arguments and passes them to the various methods to read and write data
    params: args - all possible arguments (built by the create_command_line_args method)
    """
    
    #check if file arg has been passed by user
    if args.file is not None:
        csv_file = args.file
        #load and process data
        list_csv = load_csv(csv_file)
        data = process_csv(list_csv)
    else:
        data = None
    
    # build db table only if there is data and not a dry-run
    if data and args.dry_run is False:
        create_postgres_table(data, args)
      

def main():
    args = create_command_line_args()
    process_command_line_args(args)

if __name__ == "__main__":
    main()



