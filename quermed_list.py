from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
from datetime import datetime
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


downloadDefaultDirectory = '.'
headlessmode = False
options = webdriver.ChromeOptions()
options_test = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("--disable-renderer-backgrounding");
options.add_argument("--disable-background-timer-throttling");
options.add_argument("--disable-backgrounding-occluded-windows");
options.add_argument("--disable-client-side-phishing-detection");
options.add_argument("--disable-crash-reporter");
options.add_argument("--disable-oopr-debug-crash-dump");
options.add_argument("--no-crash-upload");
options.add_argument("--disable-gpu");
options.add_argument("--disable-extensions");
options.add_argument("--disable-low-res-tiling");
options.add_argument("--log-level=3");
options.add_argument("--silent");
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument("--headless=new")
options.add_argument("--window-position=-2400,-2400")
options_test.add_argument("--disable-search-engine-choice-screen")
prefs = {
    'download.default_directory': downloadDefaultDirectory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
}
options.add_experimental_option('prefs', prefs)
options_test.add_experimental_option('prefs', prefs)
if not headlessmode:
   selected_options = options_test
else:
   selected_options = options
driver = webdriver.Chrome(options=selected_options)
haveLogin = False
closeDriver = False
driver.get("https://queermed-deutschland.de/nach-empfehlungen-suchen/")
try:
    cookie_box = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#BorlabsCookieBox .brlbs-cmpnt-dialog-box-entrance .brlbs-cpmnt-dialog-box-buttons .brlbs-btn-accept-all")))
    cookie_box.click()
except TimeoutException as e:
    print("Couldn't find: " + str("cookie_box"))
    pass

try:
    content = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content")))
except TimeoutException as e:
    print("Couldn't find: " + str("content"))
    pass
    
try:
    filter_settings = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".filter__settings")))
except TimeoutException as e:
    print("Couldn't find: " + str("filter_settings"))
    pass
    
try:
    filter_search_container = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".filter__search-container")))
except TimeoutException as e:
    print("Couldn't find: " + str("filter_search_container"))
    pass

try:
    filter_show_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".filter__settings .filter__search-container--show-field")))
except TimeoutException as e:
    print("Couldn't find: " + str("filter_show_field"))
    pass

try:
    search = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".filter__settings .filter__search-container--show-field")))
    filter_search_button = search.find_element(By.CSS_SELECTOR, "button.filter__search-button")
    filter_search_field = search.find_element(By.CSS_SELECTOR, "div.filter__search-field-container .filter__search-field")
    filter_search_field.send_keys("Psychotherapie")
    filter_search_button.click()
except TimeoutException as e:
    print("Couldn't find: " + str("search"))
    pass

try:
    psychotherapie = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".filter__value-button.button[data-id='qm_category-psychotherapie']")))
    psychotherapie.click()
except TimeoutException as e:
    print("Couldn't find: " + str("psychotherapie"))
    pass

try:
    load_more = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content .load-more")))
    content = driver.find_element(By.CSS_SELECTOR, "#content")
    qmRec = """
function qmRec() { 
	console.log("qm rec"); 

	var newTheras = [];

	var openTheras = [];
	
	var priv = createLiElement("privat");
	
	var ges = createLiElement("gesetzlich");
	
	var ges_priv = createLiElement("gesetzlich_privat");

	var privatTheras = [ ];

	var gesetzlichTheras = [ ];
	
	var gesetzlich_privat_theras = [ ];

	function createLiElement(elementTitle) {
		var ul = document.createElement('li');
		ul.setAttribute('id',elementTitle + "Li");
		ul.setAttribute('style','transition-delay: 0s');
		ul.classList.add('list__item');
		ul.classList.add(elementTitle);
		ul.innerHTML = '<div class="list__item-header header"><div class="header__arrows"></div><h2 class="header__title">' + elementTitle + '</h2></div>';
		ul.addEventListener("click", function(e) { 
			let newElements = document.querySelectorAll('.qm-recommendations__list.'+elementTitle+' .list__item.'+elementTitle);
			for (i = 0; i < newElements.length; ++i) {
				newElements[i].classList.toggle('hide');
			}
			document.querySelector('#gesetzlichLi').classList.toggle('hide', false);
			document.querySelector('#privatLi').classList.toggle('hide', false);
			document.querySelector('#gesetzlich_privatLi').classList.toggle('hide', false);
		});
		return ul;
	}

	function createUlElement(elementTitle) {
		var ul = document.createElement('ul');
		ul.setAttribute('id',elementTitle + "Ul");
		ul.classList.add('qm-recommendations__list');
		ul.classList.add('list');
		ul.classList.add(elementTitle);
		ul.addEventListener("click", function(e) { 
			ul.classList.toggle('hide');
		});
		return ul;
	}

	function addElementQmRec(elementTitle) {
		var target = document.querySelector("#content .qm-recommendations .qm-recommendations__container .qm-recommendations__list");
		elementul = createUlElement(elementTitle);
		target.parentNode.insertBefore(elementul, target.nextSibling);
		return document.querySelector("#"+elementTitle + "Ul");
	}

	function setTherasOpen() {
		var haveTheras = true;
	
		while(haveTheras) {
			var theras = document.querySelectorAll("#content .qm-recommendations li.list__item:not(.list__item--open)"); 

			for (i = 0; i < theras.length; ++i) {

				var thera = theras[i].querySelector("button.header__button");
	
				thera.click();
			}
		
			theras = document.querySelectorAll("#content .qm-recommendations li.list__item:not(.list__item--open)"); 
		
			haveTheras = theras.length > 0;
		}
	}

	function setTherasClose() {
		var haveTheras = true;
	
		while(haveTheras) {
			var theras = document.querySelectorAll("#content .qm-recommendations li.list__item.list__item--open"); 

			for (i = 0; i < theras.length; ++i) {

				var thera = theras[i].querySelector("button.header__button");
	
				thera.click();
			}
		
			theras = document.querySelectorAll("#content .qm-recommendations li.list__item.list__item--open"); 
		
			haveTheras = theras.length > 0;
		}
	}

	function start() {
		setTherasOpen();
		
		document.querySelector("#content .qm-recommendations .qm-recommendations__list").classList.toggle('first-tree', true);

		var theras = document.querySelectorAll("#content .qm-recommendations li.list__item");
	
		for (i = 0; i < theras.length; ++i) {

			var thera = theras[i];

			var theraContent = thera.querySelector(".list__item-content.content .content__row-top");
	
			var theraContentFurther = theraContent.querySelector(".content__container--further-informations");
	
			if (theraContentFurther === null) {
				newTheras.push(thera);
				continue;
			}
	
			var theraContentFurtherAll = theraContentFurther.querySelectorAll(".content__container-item");
	
			var furtherListTheraLove = [
				"Terminvereinbarung online (per eigener Website oder Ähnlichem)",
				"Videosprechstunde möglich (Webcam)",
			]
			
			var furtherListTheraLoveMustFound = furtherListTheraLove.length - 1; 
			var furtherListTheraLoveFounded = 0;
	
			for (j = 0; j < theraContentFurtherAll.length; ++j) {
				if ( furtherListTheraLove.indexOf(theraContentFurtherAll[j].innerHTML) !== -1 ) {
					furtherListTheraLoveFounded++;
				}
			}
			
			if ( furtherListTheraLoveFounded < furtherListTheraLoveMustFound) {
				newTheras.push(thera);
				continue;
			}
	
			var theraContentEmphohlen = theraContent.querySelector(".content__container--groups-of-people");
	
			if (theraContentEmphohlen === null) {
				newTheras.push(thera);
				continue;
			}
	
			var theraContentEmphohlenAll = theraContentEmphohlen.querySelectorAll(".content__container-item");

			var emphohlenListTheraLove = [
				"nonbinär",
				">trans*",
				"trans* Männlichkeiten",
				"männlich gelesen",
				"weiblich gelesen",
				"queer / lesbisch / schwul / bi / pan",
				"neurodivergent",
				"polyamor",
			];
			
			var emphohlenListTheraLoveMustFound = emphohlenListTheraLove.length - 4; 
			var emphohlenListTheraLoveFounded = 0;
			for (j = 0; j < theraContentEmphohlenAll.length; ++j) {
				if ( emphohlenListTheraLove.indexOf(theraContentEmphohlenAll[j].innerHTML) !== -1) {
					emphohlenListTheraLoveFounded++;
				}
			}
			
			if ( emphohlenListTheraLoveFounded < emphohlenListTheraLoveMustFound) {
				newTheras.push(thera);
				continue;
			}
	
			var theraKontakt = theraContent.querySelector(".content__contact");
	
			if (theraKontakt === null) {
				newTheras.push(thera);
				continue;
			}
	
			var theraKontaktAll = theraContentEmphohlen.querySelectorAll(".content__contact-item");
	
			for (j = 0; j < theraKontaktAll.length; ++j) {
				if ( theraKontaktAll[j].classList.indexOf('content__contact-item--email') === -1 ) {
					newTheras.push(thera);
					continue;
				}
			}
	
			var theraContentSprachen = theraContent.querySelector(".content__container--languages");
	
			if (theraContentSprachen === null) {
				newTheras.push(thera);
				continue;
			}
	
			var theraContentSprachenAll = theraContentEmphohlen.querySelectorAll(".content__container-item");
	
			var sprachenListTheraLove = [
				"Deutsch",
				"Englisch",
			];
			
			var sprachenListTheraLoveMustFound = sprachenListTheraLove.length - 1; 
			var sprachenListTheraLoveFounded = 0;
			for (j = 0; j < theraContentSprachenAll.length; ++j) {
				if ( sprachenListTheraLove.indexOf(theraContentSprachenAll[j].innerHTML) !== -1  ) {
					sprachenListTheraLoveMustFound++;
				}
			}
			
			if ( sprachenListTheraLoveMustFound < sprachenListTheraLoveMustFound ) {
				newTheras.push(thera);
				continue;
			}
	
			var theraKassenPrivat = theraContent.querySelector(".content__container--insurance-status");

			if (theraKassenPrivat === null) {
				newTheras.push(thera);
				continue;
			}

			var theraContentKassenPrivatAll = theraKassenPrivat.querySelectorAll(".content__container-item");
	
			var kasseListTheraLove = [
				"gesetzlich",
				"privat",
			];
	
			let hide = false;
			if (thera.classList.contains('list__item--open')) {
				hide = false;
			} else {
				hide = true;
			}
			thera.classList.toggle('first-tree', true);
	
			for (j = 0; j < theraContentKassenPrivatAll.length; j += 2) {
				let cur = theraContentKassenPrivatAll[j].innerHTML;
				let nex = (j + 1 < theraContentKassenPrivatAll.length) ? (theraContentKassenPrivatAll[j+1].innerHTML) : "ssssssssssssssssssssssssssss";
			    let isg = kasseListTheraLove[0].indexOf(cur) !== -1  || kasseListTheraLove[0].indexOf(nex) !== -1;
				let isp = kasseListTheraLove[1].indexOf(cur) !== -1  || kasseListTheraLove[1].indexOf(nex) !== -1;
				let isb = isg && isp;
				if (isb) {
					thera.classList.toggle('gesetzlich_privat', true);
					gesetzlich_privat_theras.push(thera);
				} else if(isg) {
					thera.classList.toggle('gesetzlich', true);
					gesetzlichTheras.push(thera);
				} else if(isp) {
					thera.classList.toggle('privat', true);
					privatTheras.push(thera);
				}
			}
	
			openTheras.push(thera);
		}

		setTherasClose();
		
		gesetzlich_privat = addElementQmRec("gesetzlich_privat");
		
		gesetzlich_privat.classList.toggle('gesetzlich_privat', true);
		
		gesetzlich_privat.classList.toggle('second', true);
		
		for (i = 0; i < gesetzlich_privat_theras.length; i++) {
			gesetzlich_privat.appendChild(gesetzlich_privat_theras[i]);
		}

		gesetzlich = addElementQmRec("gesetzlich");
		
		gesetzlich.classList.toggle('gesetzlich', true);
		
		gesetzlich.classList.toggle('second', true);
		
		for (i = 0; i < gesetzlichTheras.length; i++) {
			gesetzlich.appendChild(gesetzlichTheras[i]);
		}

		privat = addElementQmRec("privat");
		
		privat.classList.toggle('privat', true);
		
		privat.classList.toggle('second', true);

		for (i = 0; i < privatTheras.length; i++) {
			privat.appendChild(privatTheras[i]);
		}

		console.log(theras); 

		for (i = 0; i < newTheras.length; ++i) {
			newTheras[i].style="display: none";
			newTheras[i].remove();
		}
		
		newT = document.querySelector("#content .qm-recommendations ul.qm-recommendations__list.list[data-number-first-loaded-items]");
		newT.prepend(ges_priv);
		newT.prepend(ges);
		newT.prepend(priv);
		
		const style = document.createElement("style");
        style.innerHTML = `
				.qm-recommendations__list.gesetzlich_privat .list__item.gesetzlich_privat.hide,
				.qm-recommendations__list.gesetzlich .list__item.gesetzlich.hide,
				.qm-recommendations__list.privat .list__item.privat.hide {
					display: none;
				};
		`
		document.head.appendChild(style);
		newElements = document.querySelectorAll('.qm-recommendations__list.gesetzlich_privat .list__item.gesetzlich_privat');
        for (i = 0; i < newElements.length; ++i) {
            newElements[i].classList.toggle('hide', true);
        }
		newElements = document.querySelectorAll('.qm-recommendations__list.gesetzlich .list__item.gesetzlich');
        for (i = 0; i < newElements.length; ++i) {
            newElements[i].classList.toggle('hide', true);
        }
		newElements = document.querySelectorAll('.qm-recommendations__list.privat .list__item.privat');
        for (i = 0; i < newElements.length; ++i) {
            newElements[i].classList.toggle('hide', true);
        }
		document.querySelector('#gesetzlichLi').classList.toggle('hide', false);
		document.querySelector('#privatLi').classList.toggle('hide', false);
		document.querySelector('#gesetzlich_privatLi').classList.toggle('hide', false);
	}
	start();
}; 
    """
    driver.execute_script('window.reloadInterval = 0; window.currentScrollHeight = document.body.scrollHeight; ' + qmRec + '; function reloadLoadMore() { document.querySelector("#content .load-more button").click(); if (window.currentScrollHeight == document.body.scrollHeight) { clearInterval(window.reloadInterval); qmRec(); } window.currentScrollHeight = document.body.scrollHeight; window.scrollTo(0, window.currentScrollHeight); }; window.reloadInterval = setInterval(reloadLoadMore, 1000);')
except TimeoutException as e:
    print("Couldn't find: " + str("load_more"))
    pass

time.sleep(999999)

try:
    recommendations = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content .qm-recommendations")))
    theras = recommendations.find_elements(By.CSS_SELECTOR, "li.list__item")
except TimeoutException as e:
    print("Couldn't find: " + str("recommendations"))
    pass