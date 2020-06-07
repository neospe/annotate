#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
import linecache

DATA_PATH = '/home/user/data.tsv'

data_len = sum(1 for line in open(DATA_PATH))

app = Flask(__name__, template_folder='.')
app.config['WTF_CSRF_ENABLED'] = False


# annotation form
layer1_labels = [('class_0', 'negative'), ('class_1', 'positive')]
layer2_labels = [('class_0', 'class 0'), ('class_1', 'class 1'), ('class_2', 'class 2'), ('class_3', 'class 3'), ('class_4', 'class 4')]

class AnnotateForm(FlaskForm):
	layer1 = SelectField('Coarse', choices=layer1_labels, id='layer1', coerce=str)
	layer2 = SelectField('Fine', choices=layer2_labels, id='layer2', coerce=str)
	id = HiddenField(label=None)
	text = HiddenField(label=None)
	line_no = HiddenField(label=None)
	line_orig = HiddenField(label=None)
	modified = HiddenField(label=None, id='modified')
	submit_previous = SubmitField('Previous (<)', id='submit_previous')
	submit_next = SubmitField('Next (>)', id='submit_next')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = AnnotateForm()

	if form.is_submitted():

		# write line
		if form.modified.data == '1':
			new_text = '\t'.join([form.id.data, form.text.data, form.layer1.data.upper(), form.layer2.data.upper()])
			lines = open(DATA_PATH, 'r').readlines()
			lines[int(form.line_no.data) - 1] = new_text + '\n'
			out = open(DATA_PATH, 'w')
			out.writelines(lines)
			out.close()

		# continue
		if request.form.get('submit_next'):
			return redirect(request.base_url+'?line='+str(int(form.line_no.data)+1))
		
		if request.form.get('submit_previous'):
			return redirect(request.base_url+'?line='+str(int(form.line_no.data)-1))

	elif request.method == 'GET':

		# get current position
		line_no = request.args.get('line', '')
		if not line_no:
			return redirect(request.base_url+'?line=1')

		if int(line_no) < 1 or int(line_no) > data_len:
			return 'EOF'

		# read line
		line_orig = linecache.getline(DATA_PATH, int(line_no))
		id, text, label1, label2 = line_orig.strip().split('\t')

		# set form fields
		form.layer1.data = label1.lower()
		form.layer2.data = label2.lower()		
		form.id.data = id
		form.text.data = text
		form.line_no.data = line_no
		form.line_orig.data = line_orig

		return render_template('annotate.html', filename=DATA_PATH, form=form, line_no=line_no, text=text, data_len=data_len)

# optional: serve the js file
@app.route('/mousetrap.min.js')
def send_js():
	return send_from_directory('.', 'mousetrap.min.js')
