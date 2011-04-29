package glucose

import grails.test.*
import glucose.Utilities
import glucose.LocalDevEnvironments

class SSHTest extends GrailsUnitTestCase {
    protected void setUp() {
        super.setUp()
    }

    protected void tearDown() {
        super.tearDown()
    }

    void testClass() {
		assertEquals(true, Utilities.runCommand(LocalDevEnvironments.testHostname, 
												LocalDevEnvironments.testUsername, 
												LocalDevEnvironments.testPassword, 
												"/bin/ls"))
    }
}
