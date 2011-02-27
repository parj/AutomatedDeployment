groovyc -cp lib/log4j-1.2.16.jar -d bin src/*.groovy
groovy -cp lib/ant.jar:lib/ant-launcher.jar:lib/ant-jsch.jar:lib/jsch-0.1.44.jar:lib/log4j-1.2.16.jar:bin src/Glucose.groovy "$@"
