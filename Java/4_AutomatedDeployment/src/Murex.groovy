#!/usr/bin/env groovy

import static Environments.*
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
		
		if (MX == null)
			stringCommand = "cd $MX;" + command
		else
			stringCommand = "cd " + MX + ";" + command
		
		runCommand(stringCommand)
	}
}
