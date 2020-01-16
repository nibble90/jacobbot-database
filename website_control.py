from subprocess import run

def start_stop():
    choice = input("Would you like to start or stop the apache-jacobbot webserver? [Start/Stop]\n> ")
    if(choice.lower() == "start"):
        run(["sudo", "docker", "run", "-dit", "--name","apache-jacobbot", "-p", "8080:80", "-v", "/home/ubuntu/jacobbot/website:/usr/local/apache2/htdocs/", "httpd:2.4"])
    elif(choice.lower() == "stop"):
        run(["sudo", "docker", "stop", "apache-jacobbot"])
        run(["sudo", "docker", "rm", "apache-jacobbot"])
    else:
        print("Error, accepted values are 'start' or 'stop'\n")
        start_stop()

try:
    start_stop()
except:
    print("Error, do you have root permissions?")
