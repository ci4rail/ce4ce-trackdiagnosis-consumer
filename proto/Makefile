SRC_DIR=.
all: ${SRC_DIR}/go/geotagged_accel.proto.go \
 ${SRC_DIR}/python/geotagged_accel.proto.py 


prepare:
	mkdir -p go/ 

${SRC_DIR}/go/geotagged_accel.proto.go: ${SRC_DIR}/geotagged_accel.proto prepare
	protoc -I=${SRC_DIR} ${SRC_DIR}/geotagged_accel.proto --go_out=go/

${SRC_DIR}/python/geotagged_accel.proto.py: ${SRC_DIR}/geotagged_accel.proto prepare
	protoc -I=${SRC_DIR} ${SRC_DIR}/geotagged_accel.proto --python_out=../py_consumer


.PHONY: all prepare