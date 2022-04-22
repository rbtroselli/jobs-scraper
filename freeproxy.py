from bs4 import BeautifulSoup
import requests
import random


class FreeProxyCollection:

    def __init__(self, proxy_list=[]):
        # When initializing the object the list gets assigned with the method
        self.proxy_list = self.__get_proxies_list()


    def __get_proxies_list(self):
        ip_list = []
        html_text = requests.get("https://www.sslproxies.org/").text
        soup = BeautifulSoup(html_text,"lxml")
        
        # IP list on the site
        ips_rows = soup.find(class_="table table-striped table-bordered").find("tbody").find_all("tr")
        for ip_row in ips_rows:
            
            # If supports https. Reversed and added a guard
            if ip_row.find_all("td")[6].text != "yes":
                continue
            # Take IP and port
            ip = ip_row.find_all("td")[0].text+":"+ip_row.find_all("td")[1].text
            ip_list.append(ip)
        return ip_list


    def get_proxy(self):
        # If proxy list is empty get the list from the site again
        if self.proxy_list == []: 
            self.proxy_list = self.__get_proxies_list() 

        # Initialize a good var
        # Set it true and break the loop when proxy is working
        good = False
        while good != True:
            print(len(self.proxy_list))
            random_proxy = random.choice(self.proxy_list)
            self.proxy_list.remove(random_proxy)
            good = self.__working_proxy(random_proxy)
        return random_proxy


    def __working_proxy(self, proxy):
        # This method checks if the proxy is responding, and returns True or False
        try:
            # Using a random site to check
            requests.get("https://www.whatismyip.com/", proxies={"https" : proxy}, timeout=6)
            print("Successfully got a proxy!")
            print(proxy)
            return True
        except requests.exceptions.ConnectTimeout:
            print("Proxy timeout")
            return False
        except Exception as e:
            print(e)
            return False
