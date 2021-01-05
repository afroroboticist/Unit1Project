from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField

STATE_DICT = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

class StatesForm(FlaskForm):
	STATE_CHOICES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
					"Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
					"Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
					"Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
					"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
					"North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
					"Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
					"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


	state1 = SelectField(label='State 1', choices=STATE_CHOICES)
	state2 = SelectField(label='State 2', choices=STATE_CHOICES)
	state3 = SelectField(label='State 3', choices=STATE_CHOICES)
	state4 = SelectField(label='State 4', choices=STATE_CHOICES)
	state5 = SelectField(label='State 5', choices=STATE_CHOICES)
	state6 = SelectField(label='State 6', choices=STATE_CHOICES)
	
	submit = SubmitField('SUBMIT')

class YearForm(FlaskForm):
	YEAR_CHOICES = ["2009/2010","2010/2011","2011/2012","2012/2013","2013/2014",
					"2014/2015","2015/2016","2016/2017","2017/2018","2018/2019","2019/2020"]

	year = SelectField(label='Year of Interest', choices=YEAR_CHOICES)
	submit = SubmitField('DISPLAY')



   