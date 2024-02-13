SRC_DIR=.
all: ${SRC_DIR}/go/geotagged_accel.proto.go \
 ${SRC_DIR}/python/geotagged_accel.proto.py 


prepare:
	mkdir -p go/ python/
# go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

${SRC_DIR}/go/geotagged_accel.proto.go: ${SRC_DIR}/geotagged_accel.proto prepare
	protoc -I=${SRC_DIR} ${SRC_DIR}/geotagged_accel.proto --go_out=go/

${SRC_DIR}/python/geotagged_accel.proto.py: ${SRC_DIR}/geotagged_accel.proto prepare
	protoc -I=${SRC_DIR} ${SRC_DIR}/geotagged_accel.proto --python_out=python/


.PHONY: all prepare