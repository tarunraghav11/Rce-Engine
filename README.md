🚀 Remote Code Execution (RCE) Engine

A secure, scalable, LeetCode-style Remote Code Execution backend built using FastAPI, Redis, Docker, and PostgreSQL, designed with production-oriented architecture principles.

📌 Overview

This project implements a distributed Remote Code Execution system where:

Users submit code via an API or frontend

Jobs are queued asynchronously using Redis

Worker services execute code in isolated Docker containers

Execution results are stored in PostgreSQL

The frontend polls for job status updates

The system is designed with security, scalability, and isolation as core principles
