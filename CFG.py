from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuration Data
DATA_PATH = 'data'
BULK_DATA = './../data/2023-07-02_winter_cup.csv'
table_name = 'apl_meet_entry'
bucket_name = 'apl-lifter-images'
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