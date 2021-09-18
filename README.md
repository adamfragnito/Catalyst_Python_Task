# Catalyst_Python_Task
Python assignment for Catalyst IT

IMPORTANT

-host conflict with -h and --help issue

    Please use -host from command line, instead of -h as this conflicts with the default help switch for the argparse module I
    use to parse commands

    usage: user_upload.py [-h] [--file FILE] [--create_table] [--dry_run] [-u USERNAME] [-p PASSWORD] [-host HOST]

    optional arguments:
      -h, --help      show this help message and exit
      --file FILE     --file [csv file name] – this is the name of the CSV to be parsed
      --create_table  --create_table – this will cause the PostgreSQL users table to be built (and no further action will be taken)
      --dry_run       --dry_run – this will be used with the --file directive in case we want to run the script but not insert into the DB. All other functions will be  
                      executed, but the database won't be altered
      -u USERNAME     -u – PostgreSQL username
      -p PASSWORD     -p – PostgreSQL password
      -host HOST      -host – PostgreSQL host


Program Assumptions

apostraphe in email is allowed as valid format - some mail servers allow this and some don't so I made the decision to allow.

'postgres' is the assumed name of the database within the code, no port given

Program Notes

SQL Statement execution - program uses inline SQL. Probably not the best way but I didn't have an ORM (object relational mapping)
alternative so I went with this.
