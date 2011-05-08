import grails.util.GrailsUtil

import org.apache.log4j.Logger
import org.codehaus.groovy.grails.commons.ApplicationHolder
import org.codehaus.groovy.grails.commons.ConfigurationHolder

import glucose.Environment
import glucose.Server
import glucose.Utilities
import glucose.LocalDevEnvironments

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

class BootStrap {
	private static Logger logger = Logger.getLogger(BootStrap.class)
    def init = { servletContext ->
		switch(GrailsUtil.environment){
			case "development":
				logger.info("Setting up Development environments")
				glucose.LocalDevEnvironments.CreateDevEnvironments()
			break
			case "production":
			break
		}
		
		//SET UP THE GLUCOSE PATHS - These are dynamic because if the WAR file is deployed
		//The locations of the local path of deployment will defer server to server
		logger.info("Setting up glucose.localPath")
		def realPath = ApplicationHolder.application.parentContext.servletContext.getRealPath(ConfigurationHolder.config.grails.serverURL).split("/http")
		logger.trace("realPath - " + realPath)
		
		ConfigurationHolder.config.glucose.localPath = realPath[0]
		logger.trace("glucose.localPath - " + ConfigurationHolder.config.glucose.localPath)
		
		ConfigurationHolder.config.glucose.sshLogAppender = realPath[0] + "/" + ConfigurationHolder.config.glucose.sshLogAppenderFile
		logger.trace("glucose.sshLogAppender - " + ConfigurationHolder.config.glucose.sshLogAppender)
		
		//This is so that the Utilities class writes to the SSHLog file
		Utilities.createRollingSSHAppender()
	}
    def destroy = {
    }
}
