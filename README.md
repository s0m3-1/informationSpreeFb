# informationSpreeFb

## Please note this is my first proper Github-Project, so any advice is welcome! (no matter if for the code or the github-repository)
- If deepth is more than 1 it gets a little buggy, but I´m gonna fix that (1 is default)
- Needs quite a lot of RAM (not just firefox, but also the script as the friendslist/deepth gets huge)

--------------
### Requirements
1. geckodriver (https://github.com/mozilla/geckodriver/releases)
2. python3 (https://www.python.org/downloads/)
3. selenium (pip3 install selenium)

--------------
### Information/Setup
Make sure these files are in the same directory as fbFriendsCrawler.py
#### config.txt
- txt-file including the necessary configuration
  - fbEmail=email
  - fbPass=password
  - geckodriverPath=path-to-geckodriver\geckodriver.exe


#### fbprofiles.txt

- A txt-file with one facebookprofile-link in each line.
- Can either be a link with the fb id or the name
--> Please note the slightly different url
  - hxxps://www<.>facebook<.>com/profile.php?id=xxx
  - hxxps://www<.>facebook<.>com/xxx
  

--------------
### Example usage
python3 fbFriendsCrawler.py -c config.txt -f fbprofiles.txt -d 1

--------------
### Example output
	Going to load Friends for:
	-Profile1
	-Profile2

	start loading friends
	starting with: hxxps://www<.>facebook<.>com/Profile1
	Amount: 42
	->finished (Amount: 42, Time needed: ~26s)

	starting with: hxxps://www<.>facebook<.>com/Profile2
	Amount: 24
	->finished (Amount: 24, Time needed: ~18s)

	finished loading friends


	| Friends of Profile1 |

	Name: Person A
	Link:  hxxps://www<.>facebook<.>com/person.a  
	Friends: None
	Likes: None  
	Deepth 1
  
	Name: Person B 
	Link:  hxxps://www<.>facebook<.>com/person.b
	Friends: None
  	Likes: None
  	Deepth 1  
  
	...
  
  
  	| Friends of Profile2 |

	Name: Person A
	Link:  hxxps://www<.>facebook<.>com/person.a
	Friends: None
	Likes: None
	Deepth 1

	Name: Person B
	Link:  hxxps://www<.>facebook<.>com/person.b
	Friends: None
	Likes: None
	Deepth 1 
  
	...
  
  
  	Friends of Profile1
  
	Intersections with: Profile2
	--> 2
	{'hxxps://www<.>facebook<.>com/person.a', 'hxxps://www<.>facebook<.>com/person.b'}
