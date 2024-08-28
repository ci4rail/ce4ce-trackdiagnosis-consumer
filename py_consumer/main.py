import asyncio
import datetime
import timeconv
import geotagged_accel_pb2
from stream import NatsStream


SERVER = "tls://connect.ngs.global:4222"
CREDS = "../cemit.creds"
STREAM = "ce4ce-track-sim"
SUBJECT = "TRACKSIM.*.accel"

START_TIME = "2024-02-12T08:10:00+01:00"

async def main():

    start_time=datetime.datetime.fromisoformat(START_TIME)

    ns = await NatsStream.from_start_time(
        SERVER, CREDS, STREAM, SUBJECT, start_time
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

        # if df2["ts"].iloc[0] >= start_time:
        #     df = pd.concat([df, df2], axis=0)


    await ns.close()        

def decode_msg(msg):
    data = geotagged_accel_pb2.Chunk()
    data.ParseFromString(msg.data)

    print(f"Received message with ID {data.id}, deltaTs {data.deltaTs:.4f}, and {len(data.accelChunks)} accel chunks\n")
    for accel_chunk in data.accelChunks:
        print(f"  Accel chunk with timestamp {timeconv.pb_timestamp_to_local_datetime(accel_chunk.ts)} and {len(accel_chunk.samples)} samples\n")
        # print first three samples
        for sample in accel_chunk.samples[:3]:
            print(f"    Sample with x={sample.x:.4f}, y={sample.y:.4f}, z={sample.z:.4f}\n")
        print("    ...")

asyncio.run(main())