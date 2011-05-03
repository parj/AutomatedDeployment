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
        <style type="text/css" media="screen">
			body{
			font-family:"Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, Helvetica, sans-serif;
			font-size:12px;
			}
			p, h1, form, button{border:0; margin:0; padding:0;}
        	.spacer{clear:both; height:1px;}
        	/* ----------- My Form ----------- */
			.myform{
			margin:0 auto;
			width:auto;
			padding:1px;
			}
			/* ----------- stylized ----------- */
			#stylized{
			border:solid 2px #b7ddf2;
			background:#ebf4fb;
			}
			#stylized h1 {
			font-size:14px;
			font-weight:bold;
			margin-bottom:8px;
			}
			#stylized p{
			font-size:11px;
			color:#666666;
			margin-bottom:20px;
			border-bottom:solid 1px #b7ddf2;
			padding-bottom:10px;
			}
			#stylized label{
			display:block;
			font-weight:bold;
			text-align:right;
			width:140px;
			float:left;
			padding:0px 5px;
			}
			#stylized .labelFloatLeft{
			float:left;
			font-weight:bold;
			text-align:right;
			width:140px;
			margin:2px 0 20px 10px;
			}
			#stylized .small{
			color:#666666;
			display:block;
			font-size:11px;
			font-weight:normal;
			text-align:right;
			width:140px;
			}
			#stylized input{
			float:left;
			font-size:12px;
			padding:4px 2px;
			border:solid 1px #aacfe4;
			width:210px;
			margin:1px 0 20px 10px;
			}
			#stylized .inputtxtCommand{
			float:left;
			font-size:12px;
			padding:4px 2px;
			width:200px;
			margin:-26px 0px 0px 140px;
			}
			#stylized button{
			clear:both;
			margin-left:150px;
			width:200px;
			height:31px;
			background:#666666 url(img/button.png) no-repeat;
			text-align:center;
			line-height:31px;
			color:#FFFFFF;
			font-size:11px;
			font-weight:bold;
			}
			
			#stylized .submitToRemote{
			margin:0px 0px 0px 139px;
			width:200px;
			height:31px;
			padding:0px 0px;
			text-align:center;
			line-height:31px;
			font-size:11px;
			font-weight:bold;
			}
			
			/* -- For the autocomplete -- */
			.autocomplete-w1 { background:url(img/shadow.png) no-repeat bottom right; position:absolute; top:0px; left:0px; margin:6px 0 0 6px; /* IE6 fix: */ _background:none; _margin:1px 0 0 0; }
			.autocomplete { border:1px solid #999; background:#FFF; cursor:default; text-align:left; max-height:350px; overflow:auto; margin:-6px 6px 6px -6px; /* IE6 specific: */ _height:350px;  _margin:0; _overflow-x:hidden; }
			.autocomplete .selected { background:#F0F0F0; }
			.autocomplete div { padding:2px 5px; white-space:nowrap; overflow:hidden; }
			.autocomplete strong { font-weight:normal; color:#3399FF; }
        </style>
        <g:javascript library="prototype"></g:javascript>
        <g:javascript library="scriptaculous"></g:javascript>
        

        
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
				var elLog = document.getElementById("txtLog");
				var elLastTen = document.getElementById("txtLastTen");
				var elSubmit = document.getElementsByName("buttonSubmit");
				var boolRefresh = false;

				//The submit button is hidden, means command is being executed
				//Force refresh
				if (elSubmit[0].style.display == 'none') {
					boolRefresh = true
				}
				
				var xmlhttp = getXMLHTTP();
				xmlhttp.open("GET", datafile, true);
				
				xmlhttp.onreadystatechange = function() {
					//Response has been received => 4 and page exists => 200
					if (xmlhttp.readyState == 4 && xmlhttp.status == 200) { 
						//boolRefresh has been set to force refresh or values are not the same
						if (boolRefresh || elLog.value != xmlhttp.responseText) {
							boolRefresh = true;
						}
						else {
							boolRefresh = false;
						}
						//To reduce textbox scrolling, if nothing has changed do not referesh
						if (boolRefresh) {
							//Set the log
							elLog.value = xmlhttp.responseText;
							
							//Reverse the order of the sentences
							var split = xmlhttp.responseText.split(/\r?\n/);
							var combine = "";
							for (i = 0; i < 10; ++i) {
								combine = combine + split[split.length - (i + 2)] + "\n";
							}
							elLastTen.value = combine;
						}
					}
				}
				xmlhttp.send(null);
				setTimeout("readLogFile()",100);
			}

			

			function loadAll() {
				readLogFile();
				//loadSuggestions();
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
    <body onload="loadAll()">
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
