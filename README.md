# ce4ce-trackdiagnosis-consumer

Provides an example how to extract track diagnosis data from the NATS server that is used in the CE4CE project. 

You need the credentials to access the NATS server (not provided in this repo).

The NATS server provides the following streams:
* ce4celeipzig-trackdiag - the track diagnosis data (IMU and Camera) for Leipzig
  * IMU Data is compressed and encoded with protobuf, see `proto/geotagged_imu.proto`

The example `py_consumer/main_imu.py` shows how to extract the IMU data from the NATS server and decode it.

## Run example

* Edit the `py_consumer/main_imu.py` and 
  * enter the path to the credentials file in the `CREDS` variable.
  * enter your consumer name in the DURABLE variable. Select a unique name.

* Run example: `python3 py_consumer/main_imu.py`	

