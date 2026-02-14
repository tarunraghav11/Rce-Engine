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

🧠 Features Implemented

Asynchronous job submission

Status tracking (queued → running → success/failed)

Secure containerized execution

Resource-limited execution environment

Automatic DB initialization on startup

Input validation for empty code

Clean frontend with real-time polling

Graceful handling of DB startup race conditions
