# Logs Analysis Project

## Steps to test the project:
1. Make sure that you do have Vagrant & Virtual Machine installed.
2. Make sure that you have newsdata.sql in the vagrant folder.
3. In your vm run the follwing commands:
    1. psql -d news -f newsdata.sql
    2. psql -d news
    3. pip3 install psycopg2
    4. pip3 install pycodestyle
4. To see tool results run python3 tool.py
5. To check using a standerd style run pycodestyle --first tool.py

  
