#!/usr/bin/env groovy
import org.apache.log4j.Logger
import org.apache.log4j.PropertyConfigurator
import static Utilities.*

class Glucose {
	private static Logger logger = Logger.getLogger(Glucose.class);
	
	public static void main(String[] args) {
		PropertyConfigurator.configure("log4j.properties");
		
		logger.debug("Number of arguments passed - " + args.size());
		
		if (args.size() == 0) {
			System.out.println ("Missing command. To use - ");
			System.out.println ("./run.sh local Utilities.uptime");
			System.out.println ("./run.sh local Utilities.runCommand \"ls\" ");
			System.exit(1)
		}
		
		
		String environmentName = args[0];
		logger.debug("environmentName - " + environmentName)
		
		String classFunctionName = args[1]
		logger.trace("classFunctionName - " + classFunctionName)
		
		//Split the name of class and function
		String[] split=classFunctionName.split("\\.")
		String className = split[0]
		logger.trace("className - " + className)
		
		String action = split[1]
		logger.trace("action - " + action)
		
		logger.debug("First 2 arguments processed. About to load environment class - " + environmentName)
		
		//Dynamically load class
		Utilities.environment = Class.forName(environmentName)
		logger.trace(Utilities.environment.toString())
		
		def classAction = Class.forName(className)
		logger.trace(classAction.toString())
		
		//Example ./run.sh Utilities.uptime
		if (args.size() == 2) {
			logger.trace("About to run " + classAction + "." + action + "()")
			
			classAction."${action}"()
			
			logger.trace("Completed " + classAction + "." + action + "()")
		}
		//If arguments are passed - Example ./run.sh Murex.runMurexCommand "./launchmxj.app -s"
		else if (args.size() == 3) {
			String arguments = args[2]
			
			logger.trace("About to run " + classAction + "." + action + "(" + arguments + ")")
			
			//Dynamically call function
			classAction."${action}"(arguments)
			
			logger.trace("Completed " + classAction + "." + action + "(" + arguments + ")")
		}
	}
}