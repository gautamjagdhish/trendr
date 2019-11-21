# trendr
Social network with internal messaging system, message aggregations and trend analysis based on user’s posts

#### Implemented using Django

### Features:
**Homepage**: On this page, the user’s feed, i.e latest posts by other users, will appear. The user can like/unlike a post if they click on it. They can access the aforementioned pages from the homepage.  
**Trending**: On this page, the user can see the top 15 hashtags (and the number of posts) in the past 12 hours. When the user clicks on a hashtag, they are led to the view posts by hashtag page.  
**Messages**: This is the user’s inbox page, where they can read messages they received, see sent messages, write a new message or access deleted messages. Unread messages appear in bold. Implemented using [django-messages](https://github.com/arneb/django-messages)  
**View posts by user**: If the user clicks on the ID of another user, they can see all posts by that user.   
**View posts by hashtag**: Here the user can see all posts bearing the same hashtag. The user will be led to the page corresponding to any hashtag by clicking on it in a post.  
**Edit User Profile**: On this page, the user can edit their username, change password, profile picture and other personal details. The user’s profile picture is automatically compressed to a lower resolution to save disk space.  
**New Post**: Here, the user can create and post a new post, and add a hashtag to the post.  
**Liked Posts**: Here, the user can see all the posts which they liked listed in chronological order.  

### Dependencies:
- python
- Django(python framework)
- Crispy Forms(django package)

### To run:
- Download and extract the repositary
- Open a terminal inside myproject directory
- run 'python manage.py createsuperuser' and create a superuser
- Select a database of your choice and change the settings in myproject/settings.py(We used postgresql)
- run 'python manage.py runserver' to start the server at http://localhost:8000  
or
- run 'python manage.py runserver ipaddress:port' start the server at http://ipaddress:port
