#!/bin/bash
docker build -t autotrading .
docker run -v $(pwd):/app --name autotrading --restart=always -d autotrading:latest python main.py
