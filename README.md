# cimi-server-events
Microservice for generating CIMI-based SSEvents

# Description

This microservice will deploy a Redis server and a Flask-based SSE server.

Events are sent by jobs, which are scheduled at startup, according to the 
user configuration. There is one channel per job, thus any client subscribed 
to the event stream of an existing channel, will receive CIMI-based events 
whenever the conditions described in the job are met.


# User Guide

## Building the Docker Image

`docker build .`


## Configuration

By default, there's the following configuration:

```aidl
{
  "cimi_api_url": "http://cimi:8201/api",
  "port": 8000,
  "channels": [
    {
      "job": "demo.py",
      "frequency": 5
    }
  ]
}
```

Each job should have its own entry in the `channels` list, and should 
refer to the filename of the desired job.

`cimi_api_url` is the API URL of the CIMI server from where we want to 
get notifications from.

## Jobs

Jobs go into the folder `jobs`. There's an example of a job in this folder 
which sends out an event everytime a new user is added in CIMI.

New jobs should follow this Python structure, mainly, they must all have 
at least a function named `run`.


## Deploy the microservice

`docker run -d -p <desiredHostPort>:<portNumberInConfig> <dockerImageName>`

Once this is running, the event server can be accessed at `http://localhost:<desiredHostPort>/<channel>`

### Use custom config and jobs

To pass a different configuration and additional jobs during deployment, 
simply use Docker's bind mounts. For example:
 
`docker run -d -p 8000:8000 -v $(pwd)/myconf.json:/sse/config/config.json -v $(pwd)/myjobs/customJob.py:/sse/jobs/customJob.py <dockerImageName>`

## Configure a client

There is a test client in this repository, which sets up an event stream 
to the demo channel. 

To run it, simply `python test-client.py`.

For different channels, simply change the channel name inside that script.
