# NotiSmart - _A Smart and Configurable multi-threaded trigger notification engine_
### Project by Team 404: Found for Build-a-Thon Hackathon organized by IITG
#### Made using Python-Flask, MySQL, HTML, TailwindCSS and JavaScript

### Team Members
- [Karuna Sharma](https://github.com/Karunasharma09)
- [Abhinav Sinha](https://github.com/AbhiSinha08)  

### Presentations:&nbsp; [PDF](https://drive.google.com/file/d/1UzXM07sIJ5gz0jCkOs47qC-H1YZNR7c8/view) , &nbsp; [Video](https://drive.google.com/file/d/1RCuF44Y-WDSxCskHYgIEwwubK8SOY2rR/view?usp=sharing)

# Usage Guide
This Project requires the following tools:
- Python 3.6 or higher
- MySQL 80
- A Web Browser (yeah, sorry😐)

## Getting Started
### Step 0: Clone the repository and cd into the project directory
```
$ git clone https://github.com/AbhiSinha08/Build-a-Thon-Project.git
$ cd Build-a-Thon-Project
```
### Step 1: Install the dependencies listed in `requirements.txt`
```
$ pip install -r requirements.txt
```
### Step 2: Make Sure that you have a MySQL Server up and running either in your local computer or hosted remotely
If not, You can download [MySQL community](https://dev.mysql.com/downloads/) Server for your operating system from [here](https://dev.mysql.com/downloads/mysql/)  
Installation instructions for the same can be found [here](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
### Step 3. Configure the app to work perfectly as per your needs
- Open the `config.ini` file with any text editor to edit your MySQL user and password in the respective fields for the notification engine to connect to it.<br/>
*(You can also edit host and port number if the MySQL Server is hosted remotely)*
###### _The configuration file `config.ini` is pretty structured and simple to edit all your configurations in one place and not to edit everything in the code everytime._
- From here, you can also change other configurations for the app to use like -- the email account to send email notifications from, password for the admin portal, MySQL Database name for the app to use and much more...
###### The default password for the admin portal is 'admin'
- Optionally, You can also customize some notification content to send to employees for some specific triggers which don't need the entire notification text to be entered everytime. This can be done from editing the `notifications.ini` file inside the `static\` folder of the project.
### Step 4: Run
Run the Notification Engine Server by running either &nbsp; `flask run` &nbsp; **OR** &nbsp; `python app.py` &nbsp; command<br/>
By default, a flask application runs on port `5000` on `localhost`. So head over to http://localhost:5000 and start using!
### Step 4.1: :star:Star [this repository](https://github.com/AbhiSinha08/Build-a-Thon-Project) if you like our work⭐
