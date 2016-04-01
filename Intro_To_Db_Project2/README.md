# Project Submission: Tournament Results

Code submission for implementing a Swiss Tournament using a postgres db backend, with a python interface. [Project URL](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004#project_modal_3532028970)

### Requirements
Installation of [Vagrant](https://www.vagrantup.com/) and [Virtual Box](https://www.virtualbox.org/wiki/Downloads) is required. 


### Run


- Clone this repository and log in the virtual machine:

  ```sh
  cd vagrant      
  vagrant up      
  vagrant ssh     
  ```
- Navigate to the tournament directory:

  ```sh
  cd /vagrant/tournament
  ```

- Log on to Postgres SQL:

  ```sh
  psql
  ```
- Setup tournament schema:

  ```sh
  \i tournament.sql
  \q
  ```
- Execute test cases:

  ```sh
  python tournament_test.py
  ```
  
In order to enable logging; inside the file ```tournament/tournamenet.py```, modify the below line:
```python
logger.disabled = False
```
