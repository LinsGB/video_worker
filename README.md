tesseract:
 - sudo apt install tesseract-ocr
 - sudo apt install libtesseract-dev

dependecies python:
 - pip install -r requirements.txt

create venv:
 - mkdir venv
 - python -m venv ./venv

get into venv:
 - source venv/bin/activate

run:
 - fastapi dev main.py 

save dependencies:
 - source venv/bin/activate
 - pip freeze > requirements.txt