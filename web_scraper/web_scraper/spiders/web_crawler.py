# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests

def getTag(tagName, attr):
    tags = tagName.split(" ")
    for tag in tags:
        if(tag.startswith(attr)):
            return getTagValue(tag)

def getTagValue(tag):
    begin = tag.find('"')
    end = tag[begin + 1:].find('"')
    href = tag[begin + 1: end + begin + 1]
    return getURL(href)
	
def getURL(href):
    begin = href.find("'")
    end = href[begin + 1:].find("'")
    return href[begin + 1: end + begin + 1]	
	
def getData(cssID, soup):
    data = soup.find(id=cssID)
    if(data is not None):
        return data.text #to extract the text without html tags
    else:
        return ''

def PeriodicData(url, periodicData):
    if(url is not None):
        requests.post(url, data=periodicData)
    time.sleep(200)
    PeriodicData(url, periodicData)	
	
# Function to get Form Data
def getFormData(val, response):
    return {
        'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$uppnlApplication_id|' + val,
        '__EVENTTARGET': val,
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': unquote(response.css('input#__VIEWSTATE::attr(value)').extract_first()),
        '__VIEWSTATEGENERATOR': unquote(response.css("input#__VIEWSTATEGENERATOR::attr(value)").extract_first()),
        '__VIEWSTATEENCRYPTED': '',
        'ctl00$hidden1': '',
        'ctl00$ddlLanguage': 'en-US',
        'ctl00$ContentPlaceHolder1$HiddenField1': '',
        'ctl00$ContentPlaceHolder1$hdnDetail': '',
        '__ASYNCPOST': 'false'
    }
	
class SwachhBharatSpider(scrapy.Spider):
    name = 'web_crawler'
    start_urls = ["http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx"]
    custom_settings = {
        'FEED_URI': 'file://%(data_dir_path)s/scraped-data.csv',
        'FEED_FORMAT': 'csv',
        'HTTPCACHE_ENABLED': True,
        'POSTSTATS_INTERVAL': 200
    }

    def __init__(self, data_dir_path='C:/Users/user/Desktop/web-scraper/web-scraper/data', raw_dir_path='C:/Users/user/Desktop/web-scraper/web-scraper/data', url=None, *a, **kw):
        self.data_dir_path = data_dir_path
        self.url = url
        super(SwachhBharatSpider, self).__init__(*a, **kw)

    def parse(self, response):
        for state in response.css("#ContentPlaceHolder1_gvApplicationListState a").extract():
            val = unquote(getTag(state, "href"))
#This method reads the response object and creates a FormRequest that automatically includes all the pre-filled values from the form, along with the hidden ones.
            yield scrapy.FormRequest(
                'http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx',
                formdata=getFormData(val, response),
                callback=self.parse_districts
            )

    def parse_districts(self, response):
        for district in response.css('#ContentPlaceHolder1_gvApplicationListDistrict a').extract():
            val = unquote(getTag(district, "href"))

            yield scrapy.FormRequest(
                'http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx',
                formdata=getFormData(val, response),
                callback=self.parse_ulb
            )

    def parse_ulb(self, response):
        for ulb in response.css('#ContentPlaceHolder1_gvApplicationListULB a').extract():
            val = unquote(getTag(ulb, "href"))
			
            yield scrapy.FormRequest(
                'http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx',
                formdata=getFormData(val, response),
                callback=self.parse_ward
            )
	
    def parse_ward(self, response):
        all_Wards = response.css('#ContentPlaceHolder1_gvApplicationListWARD tr[class="newRowStyleReport"]:nth-child(odd)').extract()

        state = response.css("#ContentPlaceHolder1_gvSTATECommon_LinkButton1_0::text").extract_first()
        district = response.css("#ContentPlaceHolder1_gvDISTRICTCommon_lnkDISTRICT_NAME_0::text").extract_first()
        ulb = response.css("#ContentPlaceHolder1_gvULBCommon_lnkULB_NAME_0::text").extract_first()

        soup = BeautifulSoup(response.text, 'html.parser') #parse the html, that is, take the raw html text (response.text) and break it into Python objects. The second argument is the html parser

        for (i, wards) in enumerate(all_Wards):

            yield {
                'State': state,
                'District': district,
                'ULB Name': ulb,
                'Ward': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkWARD_NO_" + str(i), soup),
                'No. of Applications Received': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_RECEIVED_" + str(i), soup),
                'No. of Applications Not Verified': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_VERIFIEDNOT_" + str(i), soup),
                'No. of Applications Verified': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_VERIFIED_" + str(i), soup),
                'No. of Applications Approved': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_APPROVED_" + str(i), soup),
                'No. of Applications Approved having Aadhar No.': getData("ContentPlaceHolder1_gvApplicationListWARD_lblAPP_APPROVED_AADHAR_" + str(i), soup),
                'No. of Applications Rejected': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_REJECTED_" + str(i), soup),
                'No. of Applications Pullback': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_PULLBACK_" + str(i), soup),
                'No. of Applications Closed': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_CLOSED_" + str(i), soup),
                'No. of Constructed Toilet Photo(Uploaded)': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_CTP_" + str(i), soup),
                'No. of Constructed Toilet Photo(Approved)': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_CTP_APR_" + str(i), soup),
                'No. of Commenced Toilet Photo': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_INTER_" + str(i), soup),
                'No. of Constructed Toilet Photo through Swachhalaya': getData("ContentPlaceHolder1_gvApplicationListWARD_lnkAPP_CTSWACHHALAYA_" + str(i), soup),
            }