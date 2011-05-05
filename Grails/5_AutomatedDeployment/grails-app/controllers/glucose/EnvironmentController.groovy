package glucose

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
			
			//Get the environment variable form the list
			def environmentInstance = Environment.get(e)
			logger.debug("Environment details - " + environmentInstance.toString())
			
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
			
			if (command.equals("Custom Command")) {
				logger.trace("Started custom command")
				
				def customCommand = params['txtCommand']
				logger.debug("Custom Command - " + customCommand)
				
				classAction.runCommand(customCommand)
				
				logger.trace("Completed custom command")
			}
			else {
				logger.trace("Started ${className}.${action}")
			
				def arguments = params['txtCommand']
				logger.trace("Arguments - ${arguments}")
				
				//If argument has been provided
				if (arguments.size() > 0) {
					logger.trace("Started ${className}.\"${action}\"(${arguments})")
					classAction."${acton}"(arguments)
					logger.trace("Completed ${className}.\"${action}\"(${arguments})")
				} else {
					logger.trace("Started ${className}.\"${action}\"()")
					classAction."${action}"()
					logger.trace("Completed ${className}.\"${action}\"()")
				}

				logger.trace("Completed glucose.Utilities.${command}")
			}
		}
		logger.trace("Completed runIt")
	}
}
