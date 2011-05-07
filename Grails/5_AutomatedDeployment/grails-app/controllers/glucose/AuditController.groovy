package glucose
/**
* Copyright (c) 2011 Parjanya Mudunuri. All rights reserved.
*
* MIT Licence - http://www.opensource.org/licenses/mit-license.php
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*/

import org.apache.log4j.Logger;
import java.sql.Timestamp;

class AuditController {
	private static Logger logger = Logger.getLogger(AuditController.class)
	def scaffold = true
	
	static Audit addAudit(httpRequest, env, commandInvoked, statusOfRequest) {
		logger.trace("Started addAudit")
		
		def audit = new Audit(
							timeStamp:new java.sql.Timestamp(Calendar.getInstance().getTime().getTime()),
							environment: env.toString(),
							ipAddress: httpRequest.getRemoteAddr(),
							userAgent: httpRequest.getHeader("User-Agent"),
							command: commandInvoked,
							status: statusOfRequest,
							user: httpRequest.getRemoteUser())
		
		audit.save()
		if (audit.hasErrors()) {
			println audit.errors
			logger.error audit.errors
		}
		logger.trace("Completed addAudit")
		
		return audit
	}
}
