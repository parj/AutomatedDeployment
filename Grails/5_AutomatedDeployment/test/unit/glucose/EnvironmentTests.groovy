package glucose

import grails.test.*

class EnvironmentTests extends GrailsUnitTestCase {
    protected void setUp() {
        super.setUp()
    }

    protected void tearDown() {
        super.tearDown()
    }

    void testClass() {
		def ubuntu = new Environment(name:"Ubuntu", username:"parj", password:"pm")
		
		assertEquals(ubuntu.name, "Ubuntu")
		assertEquals(ubuntu.username, "parj")
		assertEquals(ubuntu.password, "pm")
    }
}
