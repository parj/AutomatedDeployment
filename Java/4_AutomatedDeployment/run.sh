groovyc src/*.groovy
groovy -cp lib/ant.jar:lib/ant-launcher.jar:lib/ant-jsch.jar:lib/jsch-0.1.44.jar src/Glucose.groovy "$@"
