running=0;
if [ -e logs/mydaemon.pid ]; then
	count=`ps -ef | grep -f logs/mydaemon.pid | grep -v grep | awk {'print $2'} | wc -l`
	if [ "$count" -gt 0 ]; then
		running=1
	fi
fi

if [ "$running" -eq 1 ]; then
	echo "Daemon service running. PID: `cat logs/mydaemon.pid`"
else
	echo "No services running."
	if [ -e logs/mydaemon.pid ]; then
		echo "Removing file - logs/mydaemon.pid"
		rm logs/mydaemon.pid
	fi
fi

