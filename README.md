First, create the virtual environment by the given command: 
`virtualenv -p python3 <envname>`, 

After creating the virtual environment activate it by the given command:
`source <envname>/bin/activate`

Then install the required libraries available in the requirements.txt file. 
Command to install requirements.txt file is given below. 
`pip install -r requirements.txt`

Now run migrations. 
`python manage.py migrate`

run django server by using command below: 
`python manage.py runserver`,
Then go to the server url.

If you want to check data in the admin panel run the command given below.
`python manage.py createsuperuser`
Provide username email and password. By using this creadentials you can login in admin panel.
you can open admin page on the url given below
`http://127.0.0.1:8001/admin`

Command for BUY or SELL order: 

For placing a new buy order, use command below:
`python manage.py trade N --order_type B --size <order size> --price <order price>`

For placing a new sell order, use command below:
`python manage.py trade N --order_type S --size <order size> --<order price>`


For modifying existing order:
`python manage.py trade M --order_id <order id> --size <order size> --price <order price>`


For deleting existing order:
`python manage.py trade D --order_id <order id>`
