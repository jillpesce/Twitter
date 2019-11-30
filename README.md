# Twitter
Implementation of Twitter using Django 

# Routes 
__/:__ This is the splash page, which doubles as the login/signup page.

__/logout:__ Logs the current user out.
 
__/profile?id=id:__ Loads the profile with specified id and displays profile html template.

__/hashtag/name:__ Loads the hashtag with the specified name and loads the html template.

__/delete?id=id:__ Deletes the post with specified id.

__/home:__ Loads the home page where the user can make posts and see others' posts. 

__/like?id=id:__ Likes or unlikes the post with specified id.

# Running the Server
Navigate to the root directory of the project

Run `python3 manage.py runserver` in the command line
