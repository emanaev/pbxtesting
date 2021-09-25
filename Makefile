docker:
	docker build  -t pbxtest .

test:
	docker network rm test;	docker network create test
	docker run -it --rm --hostname pbx --network test -v $(PWD)/yate:/usr/local/etc/yate:ro pbxtest

