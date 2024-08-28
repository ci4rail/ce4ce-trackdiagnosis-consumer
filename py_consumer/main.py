import asyncio
import datetime
import timeconv
import geotagged_imu_pb2
import zlib
from stream import NatsStream


#SERVER = "tls://connect.ngs.global:4222"
#CREDS = "../example.creds"
#STREAM = " ce4celeipzig-trackdiag"
SERVER = "nats://localhost:4222"
CREDS  = None
STREAM = "CE4CELeipzig"
SUBJECT = "CE4CELeipzig.FloorIMU.>"
DURABLE = "example-consumer"

#START_TIME = "2024-02-12T08:10:00+01:00"

async def main():

    ns = await NatsStream.from_durable(
        SERVER, CREDS, STREAM, SUBJECT, DURABLE
    )

    timeout = 2.0
    msg_count = 0
    while True:
        if msg_count % 20 == 0:
            print(f"loaded {msg_count} messages\n")

        msg = await ns.next_msg(timeout=timeout)
        if msg is None:
            print("No more data available\n")
            break
        msg_count += 1
        await ns.ack(msg)
        
        decode_msg(msg)

    await ns.close()        

def decode_msg(msg):
    # decompress using zlib
    uncompressed = zlib.decompress(msg.data) 

    data = geotagged_imu_pb2.GeoTaggedImu()
    data.ParseFromString(uncompressed)

    print(f"Received message with ID {data.id}, deltaTs {data.deltaTs:.4f}, and {len(data.imuChunks)} imu chunks\n")
    for imu_chunk in data.imuChunks:
        print(f"  imu chunk with timestamp {timeconv.pb_timestamp_to_local_datetime(imu_chunk.ts)}, {position_str(imu_chunk.position)} and {len(imu_chunk.samples)} samples\n")
        # print first three samples
        for sample in imu_chunk.samples[:3]:
            print(f"    Sample with x={sample.x:.4f}, y={sample.y:.4f}, z={sample.z:.4f}\n")
        print("    ...")

def position_str(position):
    return f"Position valid={position.valid}, ts={timeconv.pb_timestamp_to_local_datetime(position.ts)}, latitude={position.latitude}, longitude={position.longitude}, altitude={position.altitude}, epv={position.epv}, epv={position.epv}"

asyncio.run(main())