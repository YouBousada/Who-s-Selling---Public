## Setup
1. Create virtual environment using ```python -m venv .venv``` 
2. Activate virtual environment using ```source .venv/bin/activate``` (if on Windows us ```.venv\Scripts\activate```)
3. Run the command ```pip install -r requirements.txt``` to install dependencies
4. Install the .env from the Google drive and place it into the root directory. 
5. Rename the env.txt to simply .env (MAKE SURE THERE IS NO TXT EXTENSION)

## Running project 
1. Ensure virtual environment is always running using ```source .venv/bin/activate```. Virtual environment can be closed using ```deactivate```
2. Run the command ```python manage.py runserver```
3. Go to the local port http://127.0.0.1:8000/, might be different for you
