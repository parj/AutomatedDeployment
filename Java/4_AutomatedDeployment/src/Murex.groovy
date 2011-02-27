#!/usr/bin/env groovy

import org.apache.log4j.Logger
import static Utilities.*

class Murex {
	private static Logger logger = Logger.getLogger(Murex.class);
	
	static void checkServices() {	
		String command = "./launchmxj.app -s"
		
		logger.trace("About to run runMurexCommand (" + command + ")")
		runMurexCommand(command)	
		logger.trace("Completed runMurexCommand (" + command + ")")
	}
	
	static void start() {
		String command = "./mxg2000_launchall start"
		
		logger.trace("About to run runMurexCommand (" + command + ")")
		runMurexCommand(command)
		logger.trace("Completed runMurexCommand (" + command + ")")
		
		checkServices()
	}
	
	static void stop() {	
		String command = "./mxg2000_launchall stop"
		
		logger.trace("About to run runMurexCommand (" + command + ")")
		runMurexCommand("./mxg2000_launchall stop")		
		logger.trace("Completed runMurexCommand (" + command + ")")
	}
	
	static void runMurexCommand(command) {
		String stringCommand
		
		logger.trace("command - " + command)
		
		//If MX variable is not defined
		try {
			stringCommand = "cd ${Utilities.environment.MX};" + command
		}
		catch (groovy.lang.MissingPropertyException e) {
			stringCommand = "cd \$MX;" + command
		}
		
		logger.trace("stringCommand - " + stringCommand)

		logger.debug("About to run runMurexCommand (" + stringCommand + ")")
		
		runCommand(stringCommand)
		
		logger.debug("Completed runMurexCommand (" + stringCommand + ")")
	}
}
