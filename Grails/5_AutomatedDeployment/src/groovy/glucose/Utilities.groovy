package glucose

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

import java.util.ArrayList;

import org.apache.log4j.Logger
import glucose.Environment
import glucose.Server

class Utilities {
	private static Logger logger = Logger.getLogger(Utilities.class)
	private static Environment environment
	
	//Assumes environment variable is set
	static boolean runCommand(command) {
		logger.trace("runCommand(" + command + ")")
		
		def runStatus = true		
		//For each server run the command
		for (server in environment.servers) {
			logger.trace ("runCommand on " + server.hostname)
			def host = server.hostname
			
			def errorInRun = runCommand(host, environment.username, environment.password, command)
			
			if (!errorInRun)	//There was an error in the error
				runStatus = errorInRun
		}			
		return runStatus
	}
	
	//Separated out so that it can be integration tested
	static boolean runCommand(host, username, password, command) {
		def runStatus = true
		def ant = new AntBuilder()
		
		try {
			logger.debug("About to run on " + username + "@" + host + " \"" + command + "\"")
			
			ant.sshexec(host:host,
				password:password,
				username:username,
				command:command,
				output:"web-app/sshLogAppender.log",
				append:"yes",
				trust:"yes")
			
			logger.debug("Completed run on " + host)
		} catch (Exception e) {
			runStatus = true
			e.printStackTrace()
			logger.error(e.message)
		}	
		
		return runStatus
	}
	
	static void setEnvironment(environment) {
		this.environment = environment
	}
	
	static Environment getEnvironment() {
		return this.environment
	}
	
	//Marked with _ to be available to the web interface
	static void _uptime() {
		runCommand("uptime")
	}
	
	static void _listProcesses() {
		runCommand("ps -efu `whoami`")
	}
	
	static void _listProcesses(processStringToSearch) {
		runCommand("ps -ef | grep -i ${processStringToSearch} | grep -v grep")
	}
	
	static void _listPIDs(processStringToSearch) {
		runCommand("ps -ef | grep -i ${processStringToSearch} | grep -v grep | awk '{print \$2}' ")
	}
	
	static void _killPID(PID) {
		runCommand("kill ${PID}")
	}
	
	static void _kill9PID(PID) {
		runCommand("kill -9 ${PID}")
	}
	
	static void _fuserK(path) {
		runCommand("fuser -k ${path}")
	}
	
	static ArrayList listMethods() {
		def methods = Utilities.metaClass.methods.collect { method->method.name }.sort().unique()
		def discoveredMethods = methods.findAll { method->method.startsWith('_') && !method.startsWith('__')}
		logger.trace ("Methods found - " + discoveredMethods)
		return discoveredMethods
	}
}
