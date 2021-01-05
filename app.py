# app.py for Unit1Portfolio Project
from flask import Flask, redirect, url_for, render_template
import os
from forms.forms import StatesForm, YearForm
from forms import forms
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl 
import cartopy.crs as crs
import cartopy.feature as cfeature

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

states = []

print(states)

file_name_index = 0

STATE_DICT = forms.STATE_DICT

coords_file = 'datasets/state_coordinates.csv'
state_coords = pd.read_csv(coords_file)
student_loan_file = 'static/Final_StudentLoan_Dataset_.csv' 
student_loan_data = pd.read_csv(student_loan_file)


@app.route('/')
def index():
	return redirect(url_for('home'))

@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/compare', methods=['GET','POST'])
def compare():
	form = StatesForm()
	file_name = 'static/yourplot.png'
	print('Does file exist? ', os.path.isfile(file_name))
	if os.path.isfile(file_name):
		os.remove(file_name)
		print('Original file removed')
		print('Does file exist? ', os.path.isfile(file_name))
	global states
	if form.validate_on_submit():
		state1 = STATE_DICT[form.state1.data]
		state2 = STATE_DICT[form.state2.data]
		state3 = STATE_DICT[form.state3.data]
		state4 = STATE_DICT[form.state4.data]
		state5 = STATE_DICT[form.state5.data]
		state6 = STATE_DICT[form.state6.data]
		states=[state1, state2, state3, state4, state5, state6]
		return redirect(url_for('view_compare'))
	return render_template('compare.html',form=form)

@app.route('/view_compare', methods=['GET','POST'])
def view_compare():
	global file_name_index
	print('States in view compare ',states)

	#student_loan_data = pd.read_csv('static/Final_StudentLoan_Dataset_.csv')
	#student_loan_data['Quarter'].unique()
	def get_quarter(data):
  		return data[:2]

	def get_year(data):
  		return data[2:]

	student_loan_data['Q'] = student_loan_data['Quarter'].apply(get_quarter)
	student_loan_data['year'] = student_loan_data['Quarter'].apply(get_year)
	df = student_loan_data.drop(labels=['OPE ID','Quarter','Sum of Recipients'], axis=1)
	df['D_millions'] = round(df['Disbursements']/1000000 ,1)
	df = df.sort_values('Q') #Sorting Q value to plot in right order
	df['Diversity'] = 0
	condition = (df['State']==states[0])
	condition1 = (df['State']==states[1]) 
	condition2 = (df['State']==states[2])
	df.loc[condition, 'Diversity'] = 1
	df.loc[condition1, 'Diversity'] = 1
	df.loc[condition2, 'Diversity'] = 1
	df_cummulative = df.groupby(['year','Diversity']).sum('Disbursements')
	num_subplots = df.year.nunique()
	years = df.year.unique()
	dim_subplots = [int(num_subplots/2),2]
	def autolabel(rects, ax_plt):
	    for rect in rects:
	        height = rect.get_height()
	        ax_plt.annotate('{}M'.format(height),
	                    xy=(rect.get_x() + rect.get_width() / 2, height),
	                    xytext=(0, 3),  # 3 points vertical offset
	                    textcoords="offset points",
	                    ha='center', va='bottom', rotation=45)


	legend_list=states
	print('Our legend contains: ', states)
	bar_width = 0.15
	fig, ax = plt.subplots(dim_subplots[0],dim_subplots[1], figsize=[20,50])


	#display(refined_df[refined_df['State']=='GA'])
	year_count = 0
	for plot_row in range(dim_subplots[0]):
	  for plot_col in range(dim_subplots[1]):
	    year = years[year_count]
	    x_plot_count = df[df['year']==year].Q.nunique()
	    x_ticks_labels = df[df['year']==year].Q.unique()
	    ind = np.arange(x_plot_count)
	    #print(ind)
	    #Plotting Bars for Diverse states and then less Diverse states
	    rects1 = ax[plot_row,plot_col].bar(ind, df[(df['State']==states[0])][(df['year']==year)]['D_millions'], bar_width, color='g')
	    rects2 = ax[plot_row,plot_col].bar(ind + bar_width, df[(df['State']==states[1])][(df['year']==year)]['D_millions'], bar_width, color='b')
	    rects3 = ax[plot_row,plot_col].bar(ind + 2*bar_width, df[(df['State']==states[2])][(df['year']==year)]['D_millions'], bar_width, color='r')
	    rects4 = ax[plot_row,plot_col].bar(ind + 3*bar_width, df[(df['State']==states[3])][(df['year']==year)]['D_millions'], bar_width, color='yellow')
	    rects5 = ax[plot_row,plot_col].bar(ind + 4*bar_width, df[(df['State']==states[4])][(df['year']==year)]['D_millions'], bar_width, color='black')
	    rects6 = ax[plot_row,plot_col].bar(ind + 5*bar_width, df[(df['State']==states[5])][(df['year']==year)]['D_millions'], bar_width, color='purple')
	    rects_list = [rects1, rects2, rects3, rects4, rects5, rects6]
	    year_formated = year[:2]+'/'+year[2:]
	    ax[plot_row,plot_col].set_title('STUDENT LOAN DEBT FOR YEAR {}'.format(year_formated))
	    ax[plot_row,plot_col].legend(legend_list)
	    x_tick = (bar_width*6)/2
	    x_ticks_steps = []
	    for i in ind:
	      x_ticks_steps.append(i+(bar_width*2.5))
	    
	    ax[plot_row,plot_col].set_xticks(x_ticks_steps)
	    ax[plot_row,plot_col].set_xticklabels(x_ticks_labels)
	    for rects in rects_list:
	      autolabel(rects, ax[plot_row,plot_col])
	    year_count += 1
	file_name = 'static/img/plot_'+str(file_name_index)+'.png'
	print('File saved as: ',file_name)
	print('Does file exist? ', os.path.isfile(file_name))

	plt.savefig(file_name, bbox_inches='tight')
	file_name_index += 1
	return render_template('view_compare.html',file=file_name)


@app.route('/country_data', methods=['GET','POST'])
def country_data():
	
	form=YearForm()

	if form.validate_on_submit():
		year = form.year.data
		def get_quarter(data):
  			return data[:2]

		def get_year(data):
  			return data[2:]

		student_loan_data['Q'] = student_loan_data['Quarter'].apply(get_quarter)
		student_loan_data['year'] = student_loan_data['Quarter'].apply(get_year)
		df = student_loan_data.drop(labels=['OPE ID','Quarter','Sum of Recipients'], axis=1)
		df_cummulative = df.groupby(['year','State']).sum('Disbursements')
		df['D_millions'] = round(df['Disbursements']/1000000 ,1)
		df = df.sort_values('Q')
		df_by_year = df_cummulative.loc[year].reset_index()
		
		##########################################################################
		#Extract Disbursements from Grouped student loan data for particular year#
		##########################################################################

		state_coords['Debt'] = df_by_year['Disbursements']
		
		lon = state_coords['Latitude']
		lat = state_coords['Longitude']

		#debt1 = 30 #[i for i in range(0,len(lat))]
		#print(df_cummulative.loc['0910'])
		#print(type(df_cummulative.loc['0910']))
		debt= state_coords['Debt']
		
		figure = plt.figure(figsize=(15,12))

		ax = figure.add_subplot(1,1,1, projection=crs.PlateCarree())

		ax.stock_img()
		ax.coastlines()
		ax.add_feature(cfeature.STATES)

		ax.set_extent([-135, -66.5, 20, 55],
	              crs=crs.PlateCarree()) ## Important


		plt.scatter(x=lat, y=lon,
	            color="orangered",
	            s=debt/1000000,
	            marker="o",
	            alpha=1,
	            transform=crs.PlateCarree())


		y = [-130, -130, -130, -130]
		z = [40, 37, 32, 25]
		s = [100,500,1000, 5000]
		txt = ['$100 million','$500 million','$1 billion', '$5 billion']

		plt.scatter(x=y, y=z, color="orangered", s=s, marker='o', alpha=0.6)

		for i, tx in enumerate(txt):
		    ax.annotate(tx, (y[i], z[i]))

		file='static/img/'+year+'debt_plot_.png'
		
		plt.savefig(file, bbox_inches='tight')
		return render_template('country_data.html',form=form, file=file)


	return render_template('country_data.html', file='', form=form)

@app.route('/predict')
def predict():
	return render_template('home.html')

if __name__ == "__main__":
	app.run(debug=True)