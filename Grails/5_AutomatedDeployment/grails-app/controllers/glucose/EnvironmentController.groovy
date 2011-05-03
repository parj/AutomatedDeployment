package glucose

import org.apache.log4j.Logger

import glucose.Utilities
import glucose.Murex

class EnvironmentController {
	def scaffold = true
	private static Logger logger = Logger.getLogger(EnvironmentController.class)
	
	def runIt = {
		logger.trace("Started runIt")
		//Iterate through each selected environment
		for (String e in params['listEnvironment'].iterator()) {
			logger.trace("Environment selected - " + e.toString())
			
			def environmentInstance = Environment.get(e)
			logger.debug("Environment details - " + environmentInstance.toString())
			
			def command = params['listCommand']
			
			logger.debug("Command Selected - " + command)
				
			Utilities.setEnvironment environmentInstance
			if (command.equals("Custom Command")) {
				logger.trace("Started custom command")
				
				def customCommand = params['txtCommand']
				logger.debug("Custom Command - " + customCommand)
				
				glucose.Utilities.runCommand(customCommand)
				
				logger.trace("Completed custom command")
			}
			else {
				logger.trace("Not running custom command")
				logger.trace("Started glucose.Utilities.${command}")
				
				glucose.Utilities."${command}"()

				logger.trace("Completed glucose.Utilities.${command}")
			}
		}
		//redirect(action: "index")
		logger.trace("Completed runIt")
	}
}
