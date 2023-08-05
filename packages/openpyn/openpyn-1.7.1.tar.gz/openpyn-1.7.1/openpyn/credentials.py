from openpyn import root
import subprocess
import sys


def check_credentials():
    try:
        serverFiles = subprocess.check_output(
            "ls /opt/openpyn/credentials", shell=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    return True


def save_credentials():
    if root.verify_running_as_root() is False:
        print("Please run as 'sudo openpyn --init' the first time. root access is",
              "needed to store credentials in /opt/openpyn/credentials.")
        sys.exit()
    else:
        print("Storing credentials in '/opt/openpyn/credentials with openvpn",
              "compatible 'auth-user-pass' file format\n")

        username = input("Enter your username for NordVPN, i.e youremail@yourmail.com: ")
        password = input("Enter the password for NordVPN: ")
        command_1 = "sudo echo " + '"%s"' % username + " > /opt/openpyn/credentials"
        command_2 = "sudo echo " + '"%s"' % password + " >> /opt/openpyn/credentials"
        try:
            # create Empty file with 600 permissions
            subprocess.run("sudo touch /opt/openpyn/credentials".split())
            subprocess.check_call(command_1, shell=True)
            subprocess.check_call(command_2, shell=True)
            subprocess.check_call("sudo chmod 600 /opt/openpyn/credentials".split())

            print("Awesome, the credentials have been saved in '/opt/openpyn/credentials'\n")
        except subprocess.CalledProcessError:
            print("Your OS is not letting modify /opt/openpyn/credentials",
                  "Please run with 'sudo' to store credentials")
            subprocess.run("sudo rm /opt/openpyn/credentials".split())
            sys.exit()
    return
