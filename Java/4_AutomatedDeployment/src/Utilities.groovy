import static Environments.*

class Utilities {
	static void runCommand(command) {
		def ant = new AntBuilder()
		
		for (host in hosts) {
			ant.sshexec(host:host,
				keyfile:keyFile,
				username:user,
				command:command)
		}
	}
}
