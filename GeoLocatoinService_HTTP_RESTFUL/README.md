This software is written in golang
It is a HTTP RESTful service to calculate the distance between two coordinates.  The service will return a JSON response.

Prerequisites:
	- 1) Please install golang properly on you local machine
	- 2) This software uses the martini web framework.  For installations, please see: https://github.com/go-martini/martini

How to run:
	To run the http restful service on localhost at port 3000 (Martini's default port), do:
		go run rest-geoservices.go

	To run the test & benchmark, do:
		go test -bench=.
