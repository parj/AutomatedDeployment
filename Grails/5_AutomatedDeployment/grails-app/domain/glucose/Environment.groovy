package glucose

class Environment {

    static constraints = {
		name(blank:false, unqiue:true)
		username(blank:false)
		password(blank:false, password:true)
		MX(nullable:true)
    }
	
	static hasMany = [servers:Server]
	
	String name
	String username
	String password
	String MX
	
	public String toString() {
		return username + ":" + name + ":" + id
	}
}
