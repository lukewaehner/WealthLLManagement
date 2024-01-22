# NLP bot to answer finance questions.

## Recreate on local machine
**Install python**

Install version 3.9.6 from ([python.org](url))

**Install modules**

`pip3 install -r requirements.txt` (your directory must be the root file)

**Run the app**

`streamlit run streamlit_app.py`

## About the AI itself
Uses a Pipeline to pull a preset trained model through Pytorch. 

Can optionally enable the more **powerful** preset to get better finance-related answers within the Python file, but it will take some time to download the data as this is not a hosted project (30gbs of weight).
