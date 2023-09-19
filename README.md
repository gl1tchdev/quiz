# Install 
For app installed sqlite and enabled cookies required
```shell
apt-get install git sqlite
```
```shell 
git clone https://github.com/gl1tchdev/quiz
```
```shell
cd quiz
```
```shell
python -m venv env
```
```shell
source env/bin/activate
```
```shell
pip install -r requirements.txt
```
# Run
## Development
```shell
uvicorn main:app
```
## Production
Check this [source](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04). Create ```gunicorn.conf.py```:
```python
from multiprocessing import cpu_count
bind = 'unix:/path/to/project/quiz.sock'

workers = cpu_count() + 1

worker_class = 'uvicorn.workers.UvicornWorker'

accesslog = '/path/to/project/access_log'

errorlog =  '/path/to/project/error_log'
```
Then create daemon like it described in article:
```
...
ExecStart=/path/to/project/env/bin/gunicorn main:app --config gunicorn.conf.py
...
```
After follow instruction in source and use bind path in nginx conf
# Demo
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/CHS1VFO2fYU/0.jpg)](https://www.youtube.com/watch?v=CHS1VFO2fYU )
