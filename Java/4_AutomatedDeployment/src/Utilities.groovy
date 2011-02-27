import org.apache.log4j.Logger

class Utilities {
	static environment;
	private static Logger logger = Logger.getLogger(Utilities.class);
	
	static void runCommand(command) {
		logger.trace("runCommand(" + command + ")")
		
		def ant = new AntBuilder()
		
		for (host in environment.hosts) {
			logger.debug("About to run on " + environment.user + "@" + host + " \"" + command + "\"")
			
			ant.sshexec(host:host,
				keyfile:environment.keyFile,
				username:environment.user,
				command:command)
			
			logger.debug("Completed run on " + host)
		}
	}
	
	static void uptime() {
		runCommand("uptime")
	}
}
