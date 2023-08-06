# __name__ is bluebook.<module>
from bs4 import BeautifulSoup
import urllib.request

SPACE_FLILGHT_URL = "https://spaceflightnow.com/launch-schedule/"

class Launch():
    def __init__(self, date=None, mission=None, 
            time=None, site=None, description=None,
            window=None):
        self.date = date
        self.mission = mission
        self.time = time
        self.site = site
        self.description = description
        self.window = window

def get_current_launch_schedule():
    url = SPACE_FLILGHT_URL
    html = urllib.request.urlopen(url)
    schedule = get_launch_schedule(html)
    return schedule

def print_schedule(schedule=None):
    if schedule is None:
        schedule = get_current_launch_schedule()
    for launch in schedule:
        print("Date: {0}".format(launch.date))
        print("Mission: {0}".format(launch.mission))
        print("Time: {0}".format(launch.time))
        print("Site: {0}".format(launch.site))
        print("Description: {0}".format(launch.description))
        print("Window: {0}".format(launch.window))
        print("\n")
def get_launch_schedule(html):
    launch_schedule = []
    soup = BeautifulSoup(html, "html.parser")

    current = soup.select(".datename")[0]
    while current:
        try:
            # Select and find will only get descendents of the element
            launch = Launch()
            launch.date = current.select(".launchdate")[0].text.strip()
            launch.mission = current.select(".mission")[0].text.strip()

            div = current.find_next_sibling("div")
            while div and "datename" not in div["class"]:
                if "missiondata" in div["class"]:
                    spans = div.find_all("span")
                    for span in spans:
                        if "Launch time" in span.text:
                            launch.time = span.next_sibling.strip()
                        if "Launch site" in span.text:
                            launch.site = span.next_sibling.strip()
                        if "Launch window" in span.text:
                            launch.window = span.next_sibling.strip()
                if "missdescrip" in div["class"]:
                    launch.description = div.text.strip()
                div = div.find_next_sibling("div")
            launch_schedule.append(launch)
        except AttributeError:
            pass
        except IndexError:
            pass
        except:
            pass

        current = current.find_next_sibling("div", class_="datename")
    return launch_schedule

def main():
    print_schedule()
    #print(__name__)
    #print(__package__)

if __name__ == "__main__":
    main()
