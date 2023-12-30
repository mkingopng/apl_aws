"""
asdf
"""
from datetime import datetime


class CFG:
	DATA_PATH = './../data'
	BULK_DATA = './../data/2023-07-02_winter_cup.csv'
	table_name = 'apl_meet_entry'
	json_file_path = 'data.json'
	today = datetime.now()
	federation = 'AusPL'
	meet_name = 'Strength HQ Winter Cup'
	meet_date = '2023-07-02'
	meet_town = 'Lilydale'
	meet_state = 'VIC'
	meet_country = 'Australia'
	columns = [
		"First Name",
		"Last Name",
		"Email",
		"Phone Number",
		"Gender",
		"Equipment",
		"Event",
		"Date of Birth",
		"Next of Kin Name",
		"Next of Kin Phone Number"
	]