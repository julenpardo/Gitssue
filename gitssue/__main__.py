""" The script that makes this directory an executable script. """


from gitssue import Gitssue

with Gitssue() as app:
    app.run()
