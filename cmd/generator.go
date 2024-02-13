package main

import (
	"math/rand"
	"time"

	"github.com/ci4rail/ce4ce-trackdiagnosis-simulator/proto/go/geotagged_accel"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/types/known/timestamppb"
)

const (
	sampleRate = 400
	subChunks  = 10
)

func generateChunk(id int32, ts time.Time) ([]byte, time.Time, error) {
	samplesPerAccelChunk := sampleRate / subChunks

	accelChunks := make([]*geotagged_accel.Chunk_AccelChunk, 0)
	for subChunk := int(0); subChunk < subChunks; subChunk++ {

		pos := &geotagged_accel.Chunk_Position{
			Valid:     true,
			Latitude:  49 + (0.00001 * float64(id)),
			Longitude: 11 + (0.00002 * float64(id)),
			Altitude:  300,
			Eph:       0.5,
			Epv:       1.0,
		}

		samples := make([]*geotagged_accel.Chunk_AccelSample, 0)

		for i := 0; i < samplesPerAccelChunk; i++ {
			sample := &geotagged_accel.Chunk_AccelSample{
				X: 0.3 * (rand.Float32() - 0.5),
				Y: 0.1 * (rand.Float32() - 0.5),
				Z: 2 * (rand.Float32() - 0.5),
			}
			samples = append(samples, sample)
		}

		accelChunk := &geotagged_accel.Chunk_AccelChunk{
			Ts:       timestamppb.New(ts),
			Position: pos,
			Samples:  samples,
		}
		accelChunks = append(accelChunks, accelChunk)

		ts = ts.Add(time.Duration(1.0 / float32(sampleRate) * float32(samplesPerAccelChunk) * float32(time.Second)))
	}

	chunk := &geotagged_accel.Chunk{
		Id:          id,
		DeltaTs:     1.0 / float32(sampleRate),
		AccelChunks: accelChunks,
	}

	// Serialize the message
	data, err := proto.Marshal(chunk)
	if err != nil {
		return nil, ts, err
	}
	return data, ts, nil
}
