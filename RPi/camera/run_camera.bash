killall raspivid &> /dev/null
raspivid -o udp://10.42.0.1:5000 -w 640 -h 480 -t 0 -fps 90 -md 6
