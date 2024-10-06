# run.sh
#!/bin/sh

python3 -m flask db upgrade
exec python3 main.py