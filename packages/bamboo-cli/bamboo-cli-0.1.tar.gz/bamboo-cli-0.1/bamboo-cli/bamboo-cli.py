from __future__ import print_function
import argparse
import mechanicalsoup
from getpass import getpass
from pprint import pprint
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def isNotEmpty(s):
    return bool(s and s.strip())

def report():
    print("")
    print("Please choose a project to report to")
    browser.open("http://pandibamboo.com/hours")
    page = browser.get_current_page()
    projects = page.find("select", {"name":"project"}).find_all("option")
    projectOptions = []
    projectNames = []
    for i in range(len(projects)):
        if i != 0:
            print("["+str(i)+"] " + projects[i].text+"")
        projectOptions.append(projects[i]['value'])
        projectNames.append(projects[i].text)
    projectInput = int(input("Please choose a project: "))
    choosenProject = projectOptions[projectInput]
    description = input('Please write a description: ')
    hours = input("Please write how many hours to report(Not including minutes): ")

    while True:
        minutes = input("Now please provide how many minutes(0, 15, 30, 45): ")
        if int(minutes) in [0, 15, 30, 45]:
            break
        else:
            print(bcolors.WARNING+"Whoops! not a correct value(Choose one of these: 0, 15, 30, 45)"+bcolors.ENDC)
            continue

    browser.select_form(".addHours")
    browser['project'] = choosenProject
    browser['hours'] = int(hours)
    browser['minutes'] = int(minutes)
    browser['description'] = description
    resp2 = browser.submit_selected()

    if resp2.status_code == 200:
        print("")
        print("Great! you have reported the following:")
        print("Project: "+projectNames[projectInput])
        print("Time: "+hours+"."+minutes)
        print("Description: "+description)
    else:
        print("")
        print("Something went wrong.")



def list():
    browser.open("http://pandibamboo.com/hours")
    print()
    dateChoosen = input("Please write a date you want to see reports for(Format: 2017-12-01) - Leave blank for today: ")
    date = dateChoosen if isNotEmpty(dateChoosen) else time.strftime("%Y-%m-%d")
    page = browser.get_current_page()
    foundDate = page.find('div', {'data-date': date})
    foundHeader = foundDate.find('div', {'class': 'header'})
    sumTime = foundHeader.find('div', class_="time")

    hoursItems = foundDate.find('div', class_="hoursItems").find_all('div', class_="item")
    print()
    print(bcolors.HEADER+"############################ Date: "+ date + " - Total: "+sumTime.text+" ############################ "+bcolors.ENDC)
    for item in hoursItems:
        print()
        print(bcolors.BOLD+"Project: "+bcolors.ENDC+item.find('span', class_="project").text)
        print(bcolors.BOLD+"Time: "+bcolors.ENDC+ item.find('div', class_="time").text)
        print(bcolors.BOLD+"Description: "+bcolors.ENDC)
        for description in item.find_all("p"):
            print(description.text)
        print()
        print(bcolors.BOLD+'#############################'+bcolors.ENDC)





## MAIN STUFF(Above are functinos)
parser = argparse.ArgumentParser(description="Report to pandi bamboo")
parser.add_argument("username")
parser.add_argument("-p"),
args = parser.parse_args()
args.password = args.p if args.p else getpass("Please enter your bamboo password: ")

browser = mechanicalsoup.StatefulBrowser(
    soup_config={'features': 'html'},
    raise_on_404=True,
    user_agent='Bamboo-cli/0.1: https://github.com/Oleander2911/bamboo-cli',
)
# Uncomment for a more verbose output:
# browser.set_verbose(2)

browser.open("https://pandibamboo.com")
browser.select_form('.wrapper')
browser["email"] = args.username
browser["password"] = args.password
resp = browser.submit_selected()

# Uncomment to launch a web browser on the current page:
#browser.launch_browser()

# verify we are now logged in
page = browser.get_current_page()
loggedIn = page.find("a", class_="active")

if loggedIn:
    print('You are now logged in.')
    print()
    print(bcolors.OKBLUE+"[1] Report"+bcolors.ENDC)
    print(bcolors.OKBLUE+"[2] List reported"+bcolors.ENDC)
    print()
    choosenFunction = input("Please choose an option: ")

    if(int(choosenFunction) == 1):
        report()
    else:
        list()


