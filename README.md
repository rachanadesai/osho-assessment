# OSHO Techincal Assesment

## Getting Started

Follow these steps to get this project up and running locally.

### Prerequisites

Before you start, you have to have the following installed on your computer.

1. You have [Docker](https://www.docker.com) running
2. You have [PostgreSQL](https://www.postgresql.org/docs/12/index.html) installed

### Run the project

1. Clone the repo
   ```sh
   git clone https://github.com/rachanadesai/osho-assessment.git
   ```
2. To run the database service
    ```sh
    docker compose up -d db
    ```
3. To run the python application
    ```sh
    docker compose up --build flaskapp
    ```

### Requirenments

Create an API that tracks the configuration state(s) on a set of Internet of Things
(IoT) connected hardware devices. The configuration state is a simple JSON
document or data container object, what fields it contains is up to you. 
The API will live in the public cloud and be accessible globally.
You can choose what type of IoT device the API relates to (i.e lightbulb,
thermostat, switch) or keep it simple and generic.

The configuration state(s) could be the on/off state of the device and/or some
characteristic of the device (i.e target temperature for a thermostat, colour
temperature for a lightbulb). It is up to you to decide what state to include.

The solution should cover the following:
* An HTTP GET endpoint that retrieves the current configuration, and a
number of previous configurations
* An HTTP POST endpoint that updates the stored configuration either
partially or in its entirety
* Some way of de-duplicating multiple instances of configuration if there is a
race condition

### Implementations

Type of IoT devie is more generic.
This implementation includes two API endpoints:

* An HTTP GET endpoint that retrieves the current configuration and all previous configurations for a given device id
`GET /api/devices/<device_id>`

* An HTTP POST endpoint that adds the configuration for a given device ID. The configuration is compared to the most recent configuration for the device to determine if any changes were made. If there were no changes, the endpoint returns a message with a 400 status code. Otherwise, the new configuration is inserted into the database with a new timestamp:
`POST /api/devices/<device_id>`

To prevent duplicates, the implementation checks whether the new configuration is the same as the most recent configuration for the device by using hash of the config. If they are the same, it means that the new configuration has already been stored and there is no need to store it again. If they are different, it means that a new configuration has been submitted and it should be stored.

The implementation uses PostgreSQL to store the configurations.

### Testing

* POST API
    ```curl --request POST \
  --url http://localhost:8080/api/devices/621 \
  --header 'Content-Type: application/json' \
  --data '{
    "device_name": "lightblub",
    "config": {
			"status": true,
			"brightness": "daylight",
			"temparature": 5000
		}
    }'```

* GET API
    ```curl --request GET \
  --url http://localhost:8080/api/devices/1234
  ```

### Screenshots

Please take a look at testing screenshots [here](https://github.com/rachanadesai/osho-assessment/blob/main/screenshots) 