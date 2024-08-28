package main

import (
	"flag"
	"fmt"
	"os"
	"time"

	"github.com/rs/zerolog/log"

	"github.com/ci4rail/ce4ce-trackdiagnosis-simulator/cmd/internal/nats"
)

const (
	server  = "tls://connect.ngs.global:4222"
	stream  = "ce4ce-track-sim"
	subject = "accel"
)

func main() {

	flag.Usage = func() {
		fmt.Printf("Usage: %s <credsfile> <nodeID>\n", os.Args[0])
		os.Exit(1)
	}
	flag.Parse()

	if flag.NArg() != 2 {
		flag.Usage()
		return
	}

	creds := flag.Arg(0)
	nodeID := flag.Arg(1)

	// Connect to the NATS server
	conn, err := nats.Connect(server, nodeID, creds)
	if err != nil {
		log.Fatal().Err(err).Msg("failed to connect to nats")
	}

	ts := time.Now()
	id := int32(0)

	for {
		// Generate a chunk
		chunk, newTs, err := generateChunk(id, ts)
		if err != nil {
			log.Fatal().Err(err).Msg("failed to generate chunk")
		}
		fmt.Printf("Generated chunk %d len=%d\n", id, len(chunk))
		// Publish the chunk to the jetstream
		err = conn.PubExport(subject, chunk)
		if err != nil {
			log.Fatal().Err(err).Msg("failed to publish chunk")
		}

		ts = newTs
		id++
		time.Sleep(1000 * time.Millisecond)
	}

}
