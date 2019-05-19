# Web-Scraper

Scraping aspx form based webpage is different and slightly complex than scraping the usual websites.These types of websites usually send state data in requests and responses in order to keep track of the client's UI state.The __VIEWSTATE field is passed around with each POST request that the browser makes to the server. The server then decodes and loads the client's UI state from this data, performs some processing, computes the value for the new view state based on the new values and renders the resulting page with the new view state as a hidden field

In this project we'll be scraping data from this website - http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx

We are interested in creating a csv file where the scarped data will get saved with headers in this order		 	 	 	 	 	 	 	 	 

State | District | ULB Name | Ward | No. of Applications Received | No. of Applications Not Verified | No. of Applications Verified | No. of Applications Approved | No. of Applications Approved having Aadhar No. | No. of Applications Rejected | No. of Applications Pullback | No. of Applications Closed | No. of Constructed Toilet Photo | No. of Commenced Toilet Photo | No. of Constructed Toilet Photo through Swachhalaya

Pressing F12 opens up the developer window (Network tab)  

![](https://github.com/simran-pandey/Web-Scraper/blob/master/Screen%20captures/ss-3.PNG)

Select a state from the list and you will see that a request to "RPTApplicationSummary.aspx" has been made. Clicking on the response - RPTApplicationSummary.aspx leads you to the request details where you can see that your browser sent the state you've selected along with the __VIEWSTATE data that was in the original response from the server.

![](https://github.com/simran-pandey/Web-Scraper/blob/master/Screen%20captures/ss-4.PNG)

On further selecting the District another POST request is sent to the server. 

![](https://github.com/simran-pandey/Web-Scraper/blob/master/Screen%20captures/ss-5.PNG)

Finally on Selecting the ULB, you can see the wards under that particular ULB and that's the order of the data that we are interested in. Our spider has to simulate the user interaction of selecting State --> District --> ULB and submitting the form.

![](https://github.com/simran-pandey/Web-Scraper/blob/master/Screen%20captures/ss-6.PNG)

#Requisite tools 
* Python
    * Follow my tutorial [here](https://medium.com/@pandeysimran97/installing-anaconda-navigator-in-5-simple-steps-for-deep-learning-projects-c7c794f1768d)
* Pip - package-management system used to install and manage software packages written in Python
    * Download get-pip.py to a folder on your computer.
    * Open a command prompt and navigate to the folder containing get-pip.py.
    * Run the following command:
    * python [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
    * Pip is now installed!
- Scrapy framework - free and open-source web-crawling framework written in Python.
    * $ pip install Scrapy==1.3.3
- BeautifulSoup from bs4 library
    * $ pip install beautifulsoup4
    
#Before creating the spider we'll create a rough algorithm stating the steps that our spider will traverse:

Fetch http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx
* For each state found in the form's state list:
    * Create a POST request to RPTApplicationSummary.aspx passing the selected state and the __VIEWSTATE value
* For each District found in the resulting page:
    * Issue a POST request to RPTApplicationSummary.aspx passing the selected state, selected district and __VIEWSTATE value
* For each ULB found in the resulting page:
    * Issue a POST request to RPTApplicationSummary.aspx passing the selected state, selected district, selected ULB and __VIEWSTATE value
* Scrape the resulting pages ward wise appending data to a CSV file

