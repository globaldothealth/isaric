# ISARIC Inventory

Inventory application that shows number of patients by country for
various conditions.

The underlying [data file](data.csv) has the following schema:

* **PatientID**: Unique patient ID
* **Condition**: Name of the condition, shown in the filter interface
* **IsPresent** (boolean): Whether condition is present
* **Country_ISO3**: Three letter ISO 3166-1 country code

## Requirements

Requires Python >= 3.10

```shell
# Create a virtual environment
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run inventory.py
```