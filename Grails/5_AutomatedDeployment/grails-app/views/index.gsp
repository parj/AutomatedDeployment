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
        <!-- Used by grails to inject in main.gsp -->
        <meta name="layout" content="main"></meta>
        <!-- Disable caching otherwise logs will be stale-->
        <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE"></META>
        <!-- Custom Glucose CSS Code -->
        <link type="text/css" rel="stylesheet" href="css/layout.css"/>
        <!-- Used by YUI library -->
		<link type="text/css" rel="stylesheet" href="css/yui/fonts-min.css" />
		<!-- Used by GRAILS for AJAX code -->
        <g:javascript library="prototype"></g:javascript>
        <!-- Used by GRAILS -->
        <g:javascript library="scriptaculous"></g:javascript>
        <!-- YUI Library -->
        <g:javascript library="yui-min"></g:javascript>
        <!-- Custom glucose ajax code -->
		<script type="text/javascript" src="js/glucose_ajax.js"></script>
		<!-- For displaying a little spinner icon automatically when executing an AJAX command-->
		<script type="text/javascript">
			// Cannot be placed inside a .js file hence over here
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
	        	<div class="topmenu">
		    		<a href="environment/list">List Environments</a> | <a href="server/list">List Servers</a>
		    	</div>
	        	
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
		          	<select name="listCommand" id="listCommand" onchange="changeTxtCommand()">
		          		<OPTGROUP LABEL="Utilities">
		           			<g:each var="command" in="${glucose.Utilities.listMethods()}">
		           				<!-- Set the value to class name & function Ex. Utilities._uptime.
		           					 However for easier readibility set the label to just _uptime, 
		           					 but strip out the underscore. Hence the substring in label -->
		            			<option value="Utilities.${command}" label="${command.substring(1, command.size())}"></option>
		            		</g:each>
		            	</OPTGROUP>
		            	<OPTGROUP LABEL="Custom">
		            		<option selected="selected">Custom Command</option>
		            	</OPTGROUP>
		           	</select>
		           	<!--  Custom input text command -->
		           	<div class="inputtxtCommand">
			           	<!-- Custom command text field, will only be visible if Custom Command is selected -->
			           	<input name="txtCommand" id="txtCommand" size="35" placeholder="Execute Custom Command, Ex. ls " type="search" list="commonCommands"></input>
			 		</div>
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
	    		<input type="button" id="buttonRefresh" onclick="readLogFile(true);" value="Click to Refresh (only if Required)"></input>
	    	</div>
	    	<div class="spacer"></div>
	    </div>
    </body>
</html>
