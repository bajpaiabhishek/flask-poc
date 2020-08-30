On Landing page you see the options to login, register, and about section.
In register, you have only 3 fields email, password, rematch password.
When user starts typing, the suggestion appears to enter valid email, as soon as email is valid suggestion disappears and border to email field becomes green.
By default register button is disabled, It enables when password is equal to re-enter password, as well as you see the suggestion to match password and when matched the border becomes green.
This is saved in MySQL database.
Already registered users can't re register. Users will be notified if they enter wrong username or password.
In Login page you can login using Google Account(Oauth) or by the user id password created in register.
'@login_required' redirects to login if someone is trying to access URL without login.
On login you see user dashboard with options to create profile/ view profile/logout.
If user tries to view profile without creating profile data he gets redirect to create profile tab.
In create profile, at first time all fields are editable, afterwards you can't change some fields(done using JS).
JS validations are there for phone number and JS validation alerts user if he tries to upload any other file than '.jpg'
This Profile data is stored in google datastore and fetched from there. (datastore from google.cloud library is used)
Profile picture is stored in google cloud storage (storage from gcloud library is used )
Have tried  to use Flask official documentation for naming conventions and project structure.
Have placed key.json use set GOOGLE_APPLICATION_CREDENTIALS="{location}\key.json" in cmd
