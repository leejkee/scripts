#!bin/bash
#
function proxy_on(){
	export ALL_PROXY=socks5://127.0.0.1:7891
	export http_proxy=http://127.0.0.1:7890
	export https_proxy=http://127.0.0.1:7890
	echo -e "proxy on"
}

function proxy_off(){
	unset ALL_PROXY
	unset http_proxy
	unset https_proxy
	echo -e "proxy off"
}
