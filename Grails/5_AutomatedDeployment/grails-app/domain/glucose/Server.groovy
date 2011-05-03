package glucose

class Server {

    static constraints = {
		name(blank:false)
		hostname(blank:false, unique:true)
    }
	
	String hostname
	String name
	
	public String toString() {
		return name + ":" + hostname + ":" + id
	}
}
