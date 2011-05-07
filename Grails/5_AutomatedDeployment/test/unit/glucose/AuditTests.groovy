package glucose

import grails.test.*

class AuditTests extends GrailsUnitTestCase {
    protected void setUp() {
        super.setUp()
    }

    protected void tearDown() {
        super.tearDown()
    }

    void testAuditClass() {
		def now = new java.sql.Timestamp(Calendar.getInstance().getTime().getTime())
		
		def audit = new Audit(
			timeStamp: now,
			environment: "TEST",
			user: "USER",
			ipAddress: "127.0.0.1",
			userAgent: "TESTBROWSER",
			command: "TESTCOMMAND",
			status: "STARTED")
		
		assertEquals(now, audit.timeStamp)
		assertEquals("TEST", audit.environment)
		assertEquals("USER", audit.user)
		assertEquals("127.0.0.1", audit.ipAddress)
		assertEquals("TESTBROWSER", audit.userAgent)
		assertEquals("TESTCOMMAND", audit.command)
		assertEquals("STARTED", audit.status)
    }
}
