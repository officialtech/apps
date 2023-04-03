set FLASK_APP=main.py
set set FLASK_DEBUG=1

.\venv\Scripts\activate
pip install -r requirements.txt
python -m flask run -p 5000
