#!/usr/bin/env groovy

if (args.size() == 0) {
	println ("Missing command. To use - ");
	println ("./run.sh stop");
	println ("./run.sh Murex.runMurexCommand \"./launchmxj.app -s\" ");
	System.exit(1)
}

println("Running " + args[0])

//Split the name of class and function
split=args[0].split("\\.")
String className = split[0]
String action = split[1]

//Dynamically load class
def cl = Class.forName(className)

//Example ./run.sh Murex.stop
if (args.size() == 1)
	cl."${action}"()
//If arguments are passed - Example ./run.sh Murex.runMurexCommand "./launchmxj.app -s"
else if (args.size() == 2) {
	arguments = args[1]
	
	println("With arguments - " + arguments)
	
	//Dynamically call function
	cl."${action}"(arguments)
}



