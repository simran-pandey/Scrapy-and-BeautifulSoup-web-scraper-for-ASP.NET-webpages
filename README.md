# Web-Scraper

Scraping aspx form based webpage is different and slightly complex than the usual websites.These types of websites usually send state data in requests and responses in order to keep track of the client's UI state.The __VIEWSTATE field is passed around with each POST request that the browser makes to the server. The server then decodes and loads the client's UI state from this data, performs some processing, computes the value for the new view state based on the new values and renders the resulting page with the new view state as a hidden field

In this Tutorial we'll be scraping data from this website - http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx

Hitting F12 opens up the developer window
![Network tab](https://drive.google.com/open?id=1uBB8aeEoKgQqsFeRoKgU0TzefcVXN-NC)

