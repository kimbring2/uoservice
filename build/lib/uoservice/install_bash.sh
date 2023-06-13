#!/bin/bash

# Define the original and replacement strings
original_string="import UoService_pb2 as UoService__pb2"
replacement_string="from uoservice.protos import UoService_pb2 as UoService__pb2"

# Specify the path to the Python file
python_file="uoservice/protos/UoService_pb2_grpc.py"

# Use sed to replace the original string with the replacement string in the Python file
sed -i "s/$original_string/$replacement_string/g" "$python_file"