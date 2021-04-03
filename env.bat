rem This file gonna make working with .venv a little bit easer 
rem without VC++14 install and ldap module compile from scratch

if not exist "application\.venv" python -m venv application\.venv

python -m pip install python_ldap-3.3.1-cp38-cp38-win_amd64.whl
python -m pip install -r application\requirements.txt