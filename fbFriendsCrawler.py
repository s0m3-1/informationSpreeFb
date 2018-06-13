# coding=utf8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time


from optparse import OptionParser

class FacebookProfile:
    def __init__(self, name=None, fbLink=None, friends=None, likes=None, deepth=0):
        self.name = name
        self.fbLink = fbLink
        self.friends = friends
        self.likes = likes
        self.deepth = deepth
        
    def __repr__(self):
        
        return self.deepth * "  " +"Name: " + self.name + "\n" +\
             self.deepth * "  " +"Link: " + self.fbLink + "\n" +\
             self.deepth * "  " +"Friends: " + str(self.friends) + "\n" +\
             self.deepth * "  " +"Likes: " + str(self.likes) +"\n"+\
             self.deepth * "  " + "Deepth " + str(self.deepth) +"\n"
             
    
    def printFriends(self):
        for friend in self.friends:
            print(friend)
    
    def printLikes(self):
        for like in self.likes:
            print(like)
    
    
    

            
            
#################################################################################################################################################################################                
        
    
class FacebookCrawler:
    LOGIN_URL = 'https://www.facebook.com/login.php'
    FRIENDS_URLS = ["/friends", "&sk=friends"]
    EXTRACT_FRIEND_ITEM = ["Freund/in hinzufügen\n", "Add Friend\n"]


    def __init__(self):
        
        
        """
        [FacebookProfile(name = "person1", fbLink = "www.facebook.com/ person1", friends = (
            FacebookProfile(name = "personA", fbLink = "www.facebook.com/ personA", friends = (
                ), likes = ()
            ) 
            FacebookProfile(name = "personB", fbLink = "www.facebook.com/ personB", friends = (
                ), likes = ()
            )
        ),
        FacebookProfile(name = "person2", fbLink = "www.facebook.com/ person2", friends = (
            FacebookProfile(name = "personA", fbLink = "www.facebook.com/ personA", friends = (
                ), likes = ()
            ) 
            FacebookProfile(name = "personB", fbLink = "www.facebook.com/ personB", friends = (
                ), likes = ()
            )
        )
        ]
        """

        
        opts = Options()
        customProfile = FirefoxProfile()
        customProfile.set_preference("dom.webnotifications.enabled", False)
        customProfile.set_preference("dom.push.enabled", False)
        opts.profile = customProfile

        
        self.fbEmail = None
        self.fbPass = None
        self.geckodriverPath = None

        
        
        self.profilesFriends = []

        self.options = self._loadArgs()
        self.loadConfig()

        self.driver = webdriver.Firefox(executable_path=self.geckodriverPath,firefox_options = opts)
        self.wait = WebDriverWait(self.driver, 10)        
        self.login(self.fbEmail, self.fbPass)
        
        self._loadFbProfiles()

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()



    def _loadArgs(self):
        parser = OptionParser()
        parser.add_option("-c", "--file-config", action="store", dest="configFile", default=None, type=str, help="Configfile with fb login and geckodriver-path")
        parser.add_option("-f", "--file-profiles", action="store", dest="fileProfiles", default=None, type=str, help="fb-Profiles to compare their friends")
        parser.add_option("-d", "--deepth", action="store", dest="deepth", default=1, type=int, help="deepth to go for loading friends")
        parser.add_option("-p", "--printOnly", action="store", dest="printFlag", default=False, type=int, help="Flag to just print friends")

        (options, _) = parser.parse_args()
        return options
    
    
    # sets the almighty list up
    # --> (FacebookProfile(name="Name1", fbLink="www.facebook.com/Name1", friends=(), likes=()),
    #        FacebookProfile(name="Name2", fbLink="www.facebook.com/Name2", friends=(), likes=()))
    def loadConfig(self):
        
        # load and set config.txt
        # -> Facebook-login
        # -> Geckodriver-Path for Windows
        with open(self.options.configFile, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if "fbEmail" in line:
                    self.fbEmail = line.split("fbEmail=")[1].strip()
                elif "fbPass" in line:
                    self.fbPass = line.split("fbPass=")[1].strip()
                elif "geckodriverPath" in line:
                    self.geckodriverPath = line.split("geckodriverPath=")[1].strip()
     
    # Gets all profiles to be compared including their names in Facebook    
    def _loadFbProfiles(self):
        with open(self.options.fileProfiles, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.driver.get(line)
                self.wait.until(EC.visibility_of_element_located((By.ID, "fb-timeline-cover-name")))
                self.profilesFriends.append(FacebookProfile(name=self.driver.find_element_by_id('fb-timeline-cover-name').text, fbLink=line.split()[0]))
        
    
    # Gets all visible friends on the current site    
    def _get_friends_list(self):
        return self.driver.find_elements(By.CSS_SELECTOR,'div[data-testid="friend_list_item"]')


    # returns a list of all friends of the profile argument
    # each friend as FacebookProfile object
    def get_friends(self, profile):
        # creates the right friends-url
        if "?id=" in profile.fbLink:
            self.driver.get(profile.fbLink + "&sk=friends")
        else:
            self.driver.get(profile.fbLink + "/friends")
            
        # continuous scroll until no more new friends loaded
        num_of_loaded_friends = len(self._get_friends_list())
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: len(self._get_friends_list()) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._get_friends_list())
                             
            except TimeoutException:
                break  # no more friends loaded
        
        results = []
        for friend in self._get_friends_list():
            # get the profile-link of the friend
            fbLink = "https://www.facebook.com/" + friend.get_attribute('innerHTML').split('href="https://www.facebook.com/')[1].split("&")[0]
            if "?fref=pb" in fbLink:
                fbLink = fbLink.split("?fref=pb")[0]
                
            # Get name of the friend
            # cuts off a couple of information included in the friend html-element
            friendsName = friend.text
            for expression in self.EXTRACT_FRIEND_ITEM:
                if expression in friend.text:
                    friendsName = friend.text.split(expression)[1]
            if "\n" in friendsName:
                results.append(FacebookProfile(friendsName.split("\n")[0],fbLink=fbLink, deepth=profile.deepth+1))
            else:
                results.append(FacebookProfile(friendsName,fbLink=fbLink, deepth=profile.deepth+1))                    
                    
        
        return results


    # loads the friends for each profile in the profile-file
    def loadFriends(self):
        currentDeepth = 0
        print("start loading friends")
        print("---------------------")
        for profile in self.profilesFriends:
            print(profile.deepth * "  " + "starting with: " + profile.fbLink)
            start = time.time()
            tmp = crawler.get_friends(profile)
            
            profile.friends = set(tmp)
            print("Amount: " + str(len(profile.friends)))
            counter = 0
            currentDeepth = profile.deepth + 1

            while currentDeepth < self.options.deepth:
                for profileDeeper in profile.friends:
                    counter += 1
                    print(profileDeeper.deepth * "  " + str(counter)+ ". starting with: " + profileDeeper.fbLink)
                    startDeep = time.time()
                    tmp = crawler.get_friends(profileDeeper)

                    profileDeeper.friends = set(tmp)
                    timeNeededDeep = time.time()-startDeep        
                    print(profileDeeper.deepth * "  " + "\t->finished (Amount: " + str(len(profileDeeper.friends)) + ", Time needed: ~" + str(int(timeNeededDeep)) + "s)")
                
                
                currentDeepth += 1
                        
            timeNeeded = time.time()-start
            print(profile.deepth * "  " + "->finished (Amount: " + str(len(profile.friends)) + ", Time needed: ~" + str(int(timeNeeded)) + "s)")
        print("finished loading friends")
        
    def printFriends(self):
        print("start printing friends")
        for key_profile in self.profilesFriends:
            print("--------------------------------------------")
            print("| Friends of " + key_profile.name + " |")
            print("--------------------------------------------")
            for profileFriends in key_profile.friends:
                print(profileFriends)
            print(len(key_profile.friends))
        print("finished printing friends")



    def printIntersections(self):
        print("start printing friends")
        excludes = set([...])

        for profile in self.profilesFriends:
            print("Friends of " + profile.name)
            excludes.add(profile)
            for otherProfile in set(self.profilesFriends).difference(excludes):
                print("\tIntersections with: " + otherProfile.name)
                
                profileFriendsSet = set()
                for profileFriend in profile.friends:
                    profileFriendsSet.add(profileFriend.fbLink)

                            
                            
                otherProfileFriendsSet = set()
                for otherProfileFriend in otherProfile.friends:
                    otherProfileFriendsSet.add(otherProfileFriend.fbLink)

                             
                print("\t--> " + str(len(profileFriendsSet&otherProfileFriendsSet)))
                print("\t"+ str(profileFriendsSet&otherProfileFriendsSet))
                
                currentDeepth = profile.deepth + 1         
                print("profile.deepth: " + str(profile.deepth))
                print("currentDeepth. " + str(currentDeepth))                
                while currentDeepth < self.options.deepth:
                    print("going deeeeeeeep")

                    for profileDeeper in profileFriend.friends:
                        profileFriendsSet = set()
                        profileFriendsSet.add(profileDeeper.fbLink)
                        
                        print(profileFriendsSet)
                        
                        for otherProfileDeeper in otherProfileFriend.friends:
                            otherProfileFriendsSet = set()
                            otherProfileFriendsSet.add(otherProfileDeeper.fbLink)
                            
                            print(otherProfileFriendsSet)
                            
                            if len(profileFriendsSet&otherProfileFriendsSet) > 0:
                                print("Friends of " + profile.name + "->" + profileDeeper.name)
                                print("Intersection with " + otherProfile.name + "->" + otherProfileDeeper.name)
                                print("\t--> " + str(len(profileFriendsSet&otherProfileFriendsSet)))
                                print("\t"+ str(profileFriendsSet&otherProfileFriendsSet))                                
                    currentDeepth += 1
                    
            
if __name__ == '__main__':
    
    crawler = FacebookCrawler()
    
    print("Going to load Friends for:")
    print("---------------------------")
    for profile in crawler.profilesFriends:
        print("-" + profile.name)
    print()
      
    crawler.loadFriends() 
    
   
    if crawler.options.printFlag == True:
        crawler.printFriends() 
    else:
        crawler.printFriends()
        crawler.printIntersections()
        
