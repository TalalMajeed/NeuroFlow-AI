# NeuroFlow

An efficient 21st-century tool made by team **technovators** for **2024 AI Challenge** that helps its clients design comprehensive and optimized solution workflows for their projects.

<img src=https://github.com/TalalMajeed/NeuroFlow-AI/blob/master/NeuroFlow/static/assets/logo-BNZQ-ew0.png alt=Logo height=200 width=200 />

## Features

-   Computer Based Web Application
-   Available on the Internet
-   Live Diagram Generation
-   Diagram & Workflow Storage
-   User Account Management
-   Colorful Flowchart Generation

## Deployment Site

Website for the application deployed:
[Click here](https://neuro-flow-ai.vercel.app/welcome) to open

## Installation

Make sure to have Python installed (3.10v at least)

Clone the repository into your desired directory on Command Prompt / Terminal

```bash
  git clone https://github.com/TalalMajeed/NeuroFlow-AI.git
```

Install Python dependencies in **requirements.txt**

```bash
  pip install -r "requirements.txt"
```

## Getting Started (Two Ways)

**1 - Running locally using SQLite:**

Open `.env` file in NeuroFlow folder in the cloned repository

Set `LOCAL` to 1, set `LOCAL_API_KEY` to your secret OpenAI API key and save changes

Start the Web Application by running in the cloned repository directory:

```bash
  python localtest.py
```

**2 - Running locally and Connecting to PostGres:**

Set the following environment variables:

`OPENAI_API_KEY` Your OpenAI's API key to configure ChatGPT-3.5-turbo model

`POSTGRES_HOST` ep-billowing-cell-a1ehg1rp-pooler.ap-southeast-1.aws.neon.tech (Link of database server)

`POSTGRES_USER` default (Database User)

`POSTGRES_PASSWORD` LJ4pdkjm3KBz (Database Password)

Ensure you have PostGreSQL installed. If not, download and install from [PostGreSQL Official Website](https://www.postgresql.org/download/)

Start PostGreSQL service from the Services app or using pgAdmin tool

Open Command Prompt / Terminal and connect to PostGreSQL Server,

```bash
  psql -U postgres
```

create a new database

```bash
  CREATE DATABASE verceldb;
```

and then exit psql

```bash
  \q
```

Navigate to your cloned repository directory and run the following command in terminal

```bash
  psql -U postgres -d verceldb -f schema.txt
```

Start the Web Application by running in the cloned repository directory:

```bash
  python localtest.py
```

## Screenshots

![App Screenshot](https://github.com/TalalMajeed/NeuroFlow-AI/blob/master/NeuroFlow/static/assets/Workflow_example.jpeg)

## Demo

App Demo: [Click here](https://github.com/TalalMajeed/NeuroFlow-AI/blob/master/NeuroFlow-Demo.mp4) to see the video

## Example for Testing

**General Description of problem/project:**
How to create a Decentralized Voting System Web Application

**Set of technologies/resources:**
Solidity, Web 3.0

**Additional Context:**
I am a student and I want to create a Decentralized voting system for my end semester project. This project should allow the admins to add new candidates and allow people to vote based on smart contract system and the etherium blockchain.

## Tech Stack

**Front-end:**

-   Vue3, Composition API
-   Vite Frontend Server
-   Vuetify Theme Library
-   Fetch API
-   HTML 5 Canvas

**Back-end:**

-   Python Flask Server
-   psycopg2 Connector
-   OpenAI Library
-   JWT Token Authentication

**Database:**

-   Vercel PostGreSQL

## Authors

-   [@bilalrana351](https://github.com/bilalrana351)
-   [@TalalMajeed](https://github.com/TalalMajeed)
-   [@Saim-Kaleem](https://github.com/Saim-Kaleem)
-   [@EznXadee](https://github.com/EznXadee)
