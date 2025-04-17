Steps to activate virutal environment:

Step 1: Navigate to your project directory (if you haven’t already)
cd /home/remlab/ps-bpt/PythonAI

Step 2: Create a virtual environment
python3 -m venv .venv
If error:  sudo apt install python3.8-venv

Step 3: Activate the virtual environment
source .venv/bin/activate

Step 4: Install your dependencies (if you have a requirements.txt)
pip install -r requirements.txt
pip install numpy pandas # or whatever you need

Step 5: Freeze your environment (later)
pip freeze > requirements.txt
