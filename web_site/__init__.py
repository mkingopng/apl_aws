"""
:Package Initialization: __init__.py can include code that initializes the
    package. This might include setting up package-level data or states that are
    needed for the package's modules to function properly.

:Simplifying Imports: It can be used to make package imports cleaner. For
    example, if your package has a module mod.py, you can import it in the
    __init__.py file, allowing users to access it directly from the package
    rather than going one level deeper.

:Controlled Exposure of Package Contents: You can control what gets exported
    when users use from package import *. This is done by defining a list named
    __all__ in the __init__.py file, which contains the names of objects the
    package will expose as its public API.

:Package Documentation: It's a good place for package-level docstrings. This
    can be a brief description of the package and its purpose.

:Package-Level Data and Functions: Sometimes, it's useful to have data or
    functions that are available across multiple modules within the package.
    These can be defined in the __init__.py file.

:Compatibility Code: For larger packages that need to maintain compatibility
    between different versions, __init__.py can contain compatibility code to
    handle differences in dependencies or Python versions.

:Subpackage Declaration: If you have a directory within your package, placing
    an __init__.py file in it makes it a subpackage. This is useful for
    organizing larger packages.

I need to OOP the tests. Then refactor the CRUD operations into a single file,
class, methods. Refactor the tests into the test folder
"""
from .dynamodb_utilities import DynamoDBHandler
from .create import add_record
from .read import read_record

# mypackage/__init__.py
from datetime import datetime

# Configuration Data
DATA_PATH = './../data'
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
