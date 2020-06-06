
# annotate

Simple text annotation tool.

Has a minimal, keyboard-based UI for text labeling along multiple dimensions. Assumes a TSV (tab-separated values) file, where each line consists of one example followed by two labels, each separated by a tab. Like this: text<tab>label<tab>label

This can easily be adapted by changing the SelectFields in the Python and in the HTML file. It uses mousetrap.js for keyboard shortcuts, which can be changed at the end of the HTML template.

##  run

- ```pip install flask flask-wtf```
- ```FLASK_APP=annotate.py flask run```
- open in browser: ```http://127.0.0.1:5000```
- go to specific example: ```http://127.0.0.1:5000/?line=12```

## limitations

- performance: ok for files < 100k lines
- not for production: form fields lack csrf protection
- no multiuser: concurrent file writing not implemented
