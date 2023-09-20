# Description
This is a gaming quiz service. In it you can both create them and pass them and compete with your friends by score. Try it: http://quiz.glitchdev.space

<p align="center">
  <img src="https://i.imgur.com/npgDfX5.jpg">
</p>

<p align="center">
  <img src="https://i.imgur.com/aECyXnI.jpg">
</p>

<p align="center">
  <img src="https://i.imgur.com/skknLp4.jpg">
</p>

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
Check this [source](https://www.vultr.com/docs/how-to-deploy-fastapi-applications-with-gunicorn-and-nginx-on-ubuntu-20-04/). Create ```gunicorn.conf.py```:
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
