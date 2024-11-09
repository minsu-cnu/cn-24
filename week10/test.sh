#!/bin/bash

echo -n '/'; curl -X 'GET' 'http://localhost:8080/' -H 'accept: application/json'; echo
echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/1' -H 'accept: application/json'; echo
echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/2' -H 'accept: application/json'; echo

echo -n 'PUT'; curl -X 'PUT' 'http://localhost:8080/paste/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "First PUT for 0"}'; echo
echo -n 'PUT'; curl -X 'PUT' 'http://localhost:8080/paste/2' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "Second PUT for 1"}'; echo

echo -n 'DELETE'; curl -X 'DELETE' 'http://localhost:8080/paste/1' -H 'accept: application/json'; echo
echo -n 'DELETE'; curl -X 'DELETE' 'http://localhost:8080/paste/2' -H 'accept: application/json'; echo

echo -n 'POST'; curl -X 'POST' 'http://localhost:8080/paste/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "First post"}'; echo
echo -n 'POST'; curl -X 'POST' 'http://localhost:8080/paste/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "Second post"}'; echo

echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/1' -H 'accept: application/json'; echo
echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/2' -H 'accept: application/json'; echo

echo -n 'PUT'; curl -X 'PUT' 'http://localhost:8080/paste/1' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "First PUT for 0"}'; echo
echo -n 'PUT'; curl -X 'PUT' 'http://localhost:8080/paste/2' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"content": "Second PUT for 1"}'; echo

echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/1' -H 'accept: application/json'; echo
echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/2' -H 'accept: application/json'; echo

echo -n 'DELETE'; curl -X 'DELETE' 'http://localhost:8080/paste/1' -H 'accept: application/json'; echo

echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/1' -H 'accept: application/json'; echo
echo -n 'GET'; curl -X 'GET' 'http://localhost:8080/paste/2' -H 'accept: application/json'; echo
