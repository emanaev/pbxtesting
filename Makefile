docker-test:
	docker build -t pbxtest .
	docker network rm test;	docker network create test
	docker run -it --rm --hostname pbx --network test pbxtest

