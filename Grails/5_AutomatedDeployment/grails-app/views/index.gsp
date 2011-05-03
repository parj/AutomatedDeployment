<!DOCTYPE html>
<!-- 
Copyright (c) 2011 Parjanya Mudunuri. All rights reserved.

MIT Licence - http://www.opensource.org/licenses/mit-license.php
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
-->

<html>
    <head>
        <title>Glucose - No es un burro!</title>
        <meta name="layout" content="main"></meta>
        <link type="text/css" rel="stylesheet" href="css/layout.css"/>
		<link type="text/css" rel="stylesheet" href="css/yui/fonts-min.css" />
        <g:javascript library="prototype"></g:javascript>
        <g:javascript library="scriptaculous"></g:javascript>
        <g:javascript library="yui-min"></g:javascript>

        
        <script type="text/javascript">
			function toggleTxtCommand() {
				var el = document.getElementById("txtCommand");
				var list = document.getElementById("listCommand");

				if (list.value == 'Custom Command') 
					el.style.display = '';
				else
					el.style.display = 'none';
			}

			function hideSubmit() {
				var el = document.getElementsByName("buttonSubmit");
				el[0].style.display = 'none';
				readLogFile();
			}

			function showSubmit() {
				var el = document.getElementsByName("buttonSubmit");
				el[0].style.display = '';
				readLogFile();
			}

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

			function readLogFile() {
				var datafile = window.location.href.substring(0, window.location.href.lastIndexOf("/") + 1) + "sshLogAppender.log"
				
				YUI().use("datasource-io", "datasource-polling", function(Y) {
				    myDataSource = new Y.DataSource.IO({source:datafile}),
					request = {
						callback : {
				            success: function(e){
								refreshLogs(e.response.results[0].responseText);
				            }
				        }	
					},
					id = myDataSource.setInterval(500, request); //Poll every 500ms
				});
			}

			//Refreshes the 2 log text areas
			function refreshLogs(feedback) {
				var elLog = document.getElementById("txtLog");
				var elLastTen = document.getElementById("txtLastTen");
				var boolRefresh = false;
				var elSubmit = document.getElementsByName("buttonSubmit");
				
	          	//The submit button is hidden, means command is being executed
            	//or values are not the same. Force Refresh.
				if (elSubmit[0].style.display == 'none' || elLog.value != feedback) {
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

			function loadAll() {
				readLogFile();
				loadSuggestions();
			}
		</script>
		
		<!-- For displaying a little spinner icon automatically when executing an AJAX command -->
		<script type="text/javascript">
			Ajax.Responders.register({
			   onCreate: function() {
			      if($('ajax-area'))
			         $('ajax-area').update('<img src="${createLinkTo(dir:'images',file:'spinner.gif')}" border="0" alt="Loading..." title="Loading..." width="16" height="16" />');
			}});
		</script>
    </head>
    <body onload="loadAll()"  class="yui3-skin-sam  yui-skin-sam">
    	<div id="stylized" class="myform">
    		<!-- FORM TO SUBMIT REQUEST -->
	        <g:form id="frmCommand">
	        	<h1>Glucose - Automated env management</h1>
	        	<p>No es un burro!</p>

	      		<!-- List all environments -->
	      		<label>Environments
	      			<span class="small">Select your environment</span>
	      		</label>
	      		<div class="input">
	        		<g:select name="listEnvironment" from="${glucose.Environment.list()}" size="5" multiple="yes" optionKey="id" optionValue="name"></g:select>
	           	</div>
	           	
	           	<!-- Commands to run -->
	           	<label>Command
	      			<span class="small">Select the command</span>
	      		</label>
	      		<div class="input">
		           	<!-- List all available commands -->
		          	<select name="listCommand" id="listCommand" onchange="toggleTxtCommand()">
		           		<g:each var="command" in="${glucose.Utilities.listMethods()}">
		            		<option>${command}</option>
		            	</g:each>
		            	<option selected="selected">Custom Command</option>
		           	</select>
	           	</div>
	           	
	           	<!--  Custom input text command -->
	           	<div class="inputtxtCommand">
		           	<!-- Custom command text field, will only be visible if Custom Command is selected -->
		           	<input name="txtCommand" id="txtCommand" size="35" placeholder="Type Custom Command, Ex. ls " type="search" list="commonCommands"></input>
		 		</div>
		 		
	           	<div class="spacer"></div>
				
				<!-- AJAX Remote Submit. It
				1/ Submits
				2/ Hides the submit button in case you are trigger friendly
				3/ After completion, unhides the submit button  -->
				<div class="submitToRemote">
 					<g:submitToRemote id="buttonSubmit" name="buttonSubmit" controller="environment" action="runIt" value="GO!" before="hideSubmit()" onComplete="showSubmit()"></g:submitToRemote>
				</div>
			</g:form>
			
			<div class="spacer"></div>
	        
	        <!-- LOGS -->
	        <label>Last 10 lines of the log file
	        	<span class="small">(Auto Refreshes):</span>
	        </label>
	        <div class="input">
	    		<textarea rows="10" cols="150" name="txtLastTen" id="txtLastTen" readonly="readonly"></textarea>
	    	</div>
	    	<label>Entire Log:
	    	<span class="small">(Auto Refreshes):</span>
	    	</label>
	    	<div class="input">
	    		<textarea rows="15" cols="150" name="txtLog" id="txtLog" readonly="readonly"></textarea>
	    	</div>
	    	
	    	<!-- Force Refresh -->
	    	<div class="submitToRemote">
	    		<input type="button" id="buttonRefresh" onclick="readLogFile();" value="Click to Refresh (only if Required)"></input>
	    	</div>
	    	<div class="spacer"></div>
	    </div>
    </body>
</html>
