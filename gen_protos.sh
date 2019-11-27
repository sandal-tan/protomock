#!/bin/sh

for file in $(ls protos/*.proto); do
    echo "Compiling ${file}"
    case $file in
        *_api.proto)
            python -m grpc_tools.protoc -Iprotos/ --grpc_python_out=protos/ --python_out=protos/ "${file}"
            ;;
        *)
            python -m grpc_tools.protoc -Iprotos/ --python_out=protos/ "${file}"
            ;;
    esac
done
