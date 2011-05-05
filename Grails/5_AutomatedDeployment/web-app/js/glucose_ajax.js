/**
* Copyright (c) 2011 Parjanya Mudunuri. All rights reserved.
*
* MIT Licence - http://www.opensource.org/licenses/mit-license.php
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*/

//When anything other than Custom Command is chosen from drop down
//The custom command txt box is hidden
function toggleTxtCommand() {
	var el = document.getElementById("txtCommand");
	var list = document.getElementById("listCommand");

	if (list.value == 'Custom Command') 
		el.style.display = '';
	else
		el.style.display = 'none';
}

//Hiding submit button during execution
function hideSubmit() {
	var el = document.getElementsByName("buttonSubmit");
	el[0].style.display = 'none';
	readLogFile();
}

//Showing submit button post execution
function showSubmit() {
	var el = document.getElementsByName("buttonSubmit");
	el[0].style.display = '';
	readLogFile();
}

//DEMISED as YUI GET is used instead
function getXMLHTTP() {
	var xmlhttp;				
	/*@cc_on @*/
	/*@if (@_jscript_version >= 5)
	  try {
	  xmlhttp=new ActiveXObject("Msxml2.XMLHTTP")
	 } catch (e) {
	  try {
	    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP")
	  } catch (E) {
	   xmlhttp=false
	  }
	 }
	@else
	 xmlhttp=false
	@end @*/
	if (!xmlhttp) {
	 try {
	  xmlhttp = new XMLHttpRequest();
	 } catch (e) {
	  xmlhttp=false;
	 }
	}

	return xmlhttp;
}

//Continuously refreshes the log textAreas
//forceRefresh is boolean, if marked true it will forcible refresh
function readLogFile(forceRefresh) {
	var datafile = window.location.href.substring(0, window.location.href.lastIndexOf("/") + 1) + "sshLogAppender.log"
	
	var xmlhttp = getXMLHTTP();
	xmlhttp.open("GET", datafile, true);
	
	xmlhttp.onreadystatechange = function() {
		//Response has been received => 4 and page exists => 200
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) { 
			refreshLogs(xmlhttp.responseText, forceRefresh);
		}
	}
	xmlhttp.send(null);
	setTimeout("readLogFile()",100);
}

//Issue with caching in Webkit - always loads from Cache. Commented out for now
//Continuously refreshes the log textAreas
//forceRefresh is boolean, if marked true it will forcible refresh
/*
function readLogFile(forceRefresh) {
	var datafile = window.location.href.substring(0, window.location.href.lastIndexOf("/") + 1) + "sshLogAppender.log"
	
	YUI().use("datasource-io", "datasource-polling", function(Y) {
	    myDataSource = new Y.DataSource.IO({source:datafile}),
		request = {
			callback : {
	            success: function(e){
					refreshLogs(e.response.results[0].responseText, forceRefresh);
	            }
	        }	
		},
		id = myDataSource.setInterval(200, request); //Poll every 500ms
	});
}*/

//Refreshes the 2 log text areas
//forceRefresh is boolean, if marked true it will forcible refresh
function refreshLogs(feedback, forceRefresh) {
	var elLog = document.getElementById("txtLog");
	var elLastTen = document.getElementById("txtLastTen");
	var boolRefresh = forceRefresh;
	var elSubmit = document.getElementsByName("buttonSubmit");
	
  	//The submit button is hidden, means command is being executed
	//or values are not the same. Force Refresh.
	if (forceRefresh || elSubmit[0].style.display == 'none' || elLog.value != feedback) {
		boolRefresh = true;
	}
	else {
		boolRefresh = false;
	}
	
	//To reduce textbox scrolling, if nothing has changed do not referesh
	if (boolRefresh) {
		//Set the log
		elLog.value = feedback;
		
		//Reverse the order of the sentences so that latest
		//is on top
		var split = feedback.split(/\r?\n/);
		var combine = "";
		for (i = 0; i < 10; ++i) {
			combine = combine + split[split.length - (i + 2)] + "\n";
		}
		elLastTen.value = combine;
	}
}

//For autosuggest. Loads from suggestions.txt for custom command text area
function loadSuggestions() {
	var datafile = window.location.href.substring(0, window.location.href.lastIndexOf("/") + 1) + "suggestions.txt"
	YUI().use("datasource-io", "datasource-textschema", function(Y) {
	    myDataSource = new Y.DataSource.IO({source:datafile}),
		myCallback = {
            success: function(e){
	            //Split using new lines
            	var suggestions = e.response.results[0].responseText.split(/\r?\n/);

				YUI().use("autocomplete", "autocomplete-filters", "autocomplete-highlighters", function (Y) {							    
					  Y.one('#txtCommand').plug(Y.Plugin.AutoComplete, {
					    resultFilters    : 'phraseMatch',
					    resultHighlighter: 'phraseMatch',
					    source           : suggestions
					  })});
				}
	    };

	    myDataSource.sendRequest({
	        request:"",
	        callback:myCallback
	    });
	});
}

//Called during Body Load
function loadAll() {
	readLogFile();
	loadSuggestions();
}

