SRC_DIR=.
all: \
 ${SRC_DIR}/python/geotagged_imu.proto.py 


# prepare:
# 	mkdir -p go/ 

# ${SRC_DIR}/go/geotagged_imu.proto.go: ${SRC_DIR}/geotagged_imu.proto prepare
# 	protoc -I=${SRC_DIR} ${SRC_DIR}/geotagged_imu.proto --go_out=go/

${SRC_DIR}/python/geotagged_imu.proto.py: ${SRC_DIR}/geotagged_imu.proto prepare
	protoc -I=${SRC_DIR} ${SRC_DIR}/geotagged_imu.proto --python_out=../py_consumer


.PHONY: all prepare