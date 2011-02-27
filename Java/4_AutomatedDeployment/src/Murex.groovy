#!/usr/bin/env groovy

import static Utilities.*

class Murex {
	static void checkServices() {	runMurexCommand("./launchmxj.app s")	}
	
	static void start() {
		runMurexCommand("./mxg2000_launchall start")
		checkServices()
	}
	
	static void stop() {	runMurexCommand("./mxg2000_launchall stop")		}
	
	static void runMurexCommand(command) {
		String stringCommand
		
		//If MX variable is not defined
		try {
			stringCommand = "cd ${Utilities.environment.MX};" + command
		}
		catch (groovy.lang.MissingPropertyException e) {
			stringCommand = "cd \$MX;" + command
		}

		runCommand(stringCommand)
	}
}
