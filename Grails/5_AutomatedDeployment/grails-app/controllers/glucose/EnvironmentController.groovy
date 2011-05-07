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

import org.apache.log4j.Logger

import glucose.Utilities
import glucose.Murex

class EnvironmentController {
	def scaffold = true
	private static Logger logger = Logger.getLogger(EnvironmentController.class)
	
	def runIt = {
		logger.trace("Started runIt")

		//Iterate through each of the selected environment
		for (String e in params['listEnvironment'].iterator()) {
			logger.trace("Environment selected - " + e.toString())
			
			//Get the environment variable from the list
			def environmentInstance = Environment.get(e)
			logger.debug("Environment details - " + environmentInstance.toString())
			
			//Add audit - Event START
			AuditController.addAudit(request,	//HTTPRequest
				environmentInstance.toString(),	//Environment running against
				params['listCommand'] + "(" + params['txtCommand'] + ")", //Command
				"Started"						//Status
			)
			
			//Get the command selected
			def command = params['listCommand']
			logger.debug("Command Selected - " + command)
			
			//Split the name of class and function - Example - Utilities._upTime()
			String[] split=command.split("\\.")
			String className = "glucose." + split[0] //Prepending glucose as package is glucose
			logger.trace("className - " + className)
			String action = split[1]
			logger.trace("action - " + action)
			
			//Dynamically load class
			//Specific Classloader needs to be specified for Grails
			//See - http://grails.1312388.n4.nabble.com/ClassNotFoundException-with-Class-forName-td1350456.html
			logger.trace("About to dyamically load ${className}")
			def classAction = Class.forName(className, false, EnvironmentController.class.classLoader)
			
			logger.trace("Setting environment " + environmentInstance.toString())
			Utilities.setEnvironment environmentInstance
		
			def arguments = params['txtCommand']
			logger.debug("Arguments - ${arguments}")
			
			//If argument has been provided
			if (arguments.size() > 0) {
				logger.trace("Started ${className}.\"${action}\"(${arguments})")
				classAction."${action}"(arguments)
				logger.trace("Completed ${className}.\"${action}\"(${arguments})")
			} else {
				logger.trace("Started ${className}.\"${action}\"()")
				classAction."${action}"()
				logger.trace("Completed ${className}.\"${action}\"()")
			}
			
			//Add audit - Event COMPLETE
			AuditController.addAudit(request,	//HTTPRequest
				environmentInstance.toString(),	//Environment running against
				params['listCommand'] + "(" + params['txtCommand'] + ")", //Command
				"Completed"						//Status
			)
		}
		logger.trace("Completed runIt")
	}
}
