package glucose

import org.hibernate.validator.AssertFalse;

import grails.test.*

class ServerTests extends GrailsUnitTestCase {
    protected void setUp() {
        super.setUp()
    }

    protected void tearDown() {
        super.tearDown()
    }

    void testClass() {
		def localhostServer = new Server(name: "Ubuntu", hostname: "localhost")
		
		assertEquals(localhostServer.name, "Ubuntu")
		assertEquals(localhostServer.hostname, "localhost")
    }
}
