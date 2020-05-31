relationships need:
	backref -- point to table with relationship
	cascade="all,delete"
	
if delete-orphan is added, peices of data get removed that might be needed later; this warrants manual checking
