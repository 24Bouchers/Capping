# Appy.py

Appi.py Api is a collaborative capping (Capstone) projects from five students at Marist College For GTel.

Steven Boucher
Easton Eberwein
Nick Vasquez
Liam Haggerty
Christian Bauer

## Table of Contents

- [Introduction](#introduction)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Parameters](#parameters)
- [Responses](#responses)
- [Rate Limiting](#rate-limiting)
- [Errors](#errors)
- [Examples](#examples)
- [License](#license)

## Introduction

The purpose of this API is to allow Gtel Employees to insert static IP addresses through their website and verify through
their free radius servers. This webpage also displays relevant data about their servers, connectivity, MAC addresses, and IP Addresses.  

## Authentication

Explain how to authenticate when using the API. Include details about API keys, tokens, or any other necessary authentication methods.

## Endpoints

The API currently connects to a web server (http://10.10.9.40:5000) and a MariaDB server (10.10.9.43) both hosted by Marist College.
Ultimately, These servers will be on Gtel/ArchtopFiber Servers.

### Endpoint 1

- **http://10.10.9.40:5000:** `/endpoint1`
- **Method:** GET
- **Description:** Description of what this endpoint does.
- **Parameters:**
  - `param1` (Type): Description
- **Example Request:**

GET /endpoint1?param1=value

