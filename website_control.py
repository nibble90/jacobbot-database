from subprocess import run

def start_stop():
    choice = input("Would you like to start or stop the nginx-jacobbot webserver? [Start/Stop]\n> ")
    if(choice.lower() == "start"):
        #run(["sudo", "docker", "run", "-dit", "--name","apache-jacobbot", "-p", "8080:80", "-v", "/home/ubuntu/jacobbot/website:/usr/local/apache2/htdocs/", "httpd:2.4"])
        run(["python3", "app.py"])
    elif(choice.lower() == "stop"):
        pass
        #run(["sudo", "docker", "stop", "apache-jacobbot"])
        #run(["sudo", "docker", "rm", "apache-jacobbot"])
    else:
        print("Error, accepted values are 'start' or 'stop'\n")
        start_stop()

if __name__ == "__main__":
    try:
        start_stop()
    except:
        print("Error, do you have root permissions?")
