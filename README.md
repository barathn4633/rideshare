# DJANGO car pool system
## payment with blockchain
### Installation
requires python > 3 django 1.9

After cloning repo

```sh
cd Carpool
python manage.py makemigrations
python manage.py migrate
```

### Create superuser
creates the admin account

```sh
python manage.py createsuperuser
Username:
Email Address:
Password:
Password (again):
```

###Coniguring Email
-Open settings.py

```python
#replace with gmail username and password or comment out to ignore the email
STATIC_URL = '/static/'
ACCOUNT_ACTIVATION_DAYS=7
EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS=1
EMAIL_PORT=587
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

```

-Open views.py line 85
edit the email address there or comment out the line to ignore sending emails in contact form
```python
def contact(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        website = request.POST['website']
        message = request.POST['message']

        send_message = '''
        Name : %s
        Email : %s
        Website : %s
        Message : %s

        ''' % (name, email, website, message)

        send_mail('Contact Form Message From My Ride', send_message, 'daviduchenna@outlook.com', ['daviduchenna@outlook.com'])
        if request.user.is_authenticated():
            return render(request, 'app/contact_loggedin.html',{'done':True})
        else:
            return render(request, 'app/contact.html',{'done':True})

    if request.user.is_authenticated():
        return render(request, 'app/contact_loggedin.html')
    else:
        return render(request, 'app/contact.html')




```




### Running the server

```sh
python manage.py runserver 
```
Open browser to
http://localhost:8000/

### Todos

 - [x] Notifications
 - [x] Chat Integration (personal and group messaging)
 - [x] Add liscence registration for drivers
 - [ ] Add Agency registration for hired cars
 - [x] Inbox and notification menus

