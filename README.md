Project "Comments".
This is a one-page application that allows you to both create new comments and reply to existing comments on any topic. To post a comment, you need to fill out a form - indicate your username and email. You can attach images and text files to your post:
- the image must be no more than 320x240 pixels (it will be automatically reduced to the specified dimensions if you try to place a larger image);
- the text file should not be more than 100 kb, TXT format.
- the following html tags are allowed in the comment text: “i”, “strong”, “code”, “a”.

The main page displays a list of comments that indicate the start of a new topic. The user can expand the entire topic thread by clicking on the corresponding button.
Calling the form for posting a comment is available through the "Новая тема" button - to start a new topic or through the "Форма ответа" button - to respond to an existing comment.

To run the project use the following commands:
Install requirements:
```shell
pip install requirements.txt
```
Run migrations:
```shell
python manage.py migrate
```
Run server:
```shell
python manage.py runserver
```