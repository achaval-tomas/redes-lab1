#!/bin/bash

curl --data "@put.json" --header "Content-Type: application/json" --request PUT http://localhost:5000/peliculas/$1