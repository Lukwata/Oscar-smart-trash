import time

import numpy as np
from grpc.beta import implementations

from apis import (prediction_service_pb2, predict_pb2, dtypes, tensor_pb2,
                  tensor_util)


def main():
    host = "192.168.1.113"
    port = 9000

    image_path = "00079.jpg"
    with open(image_path, "rb") as f:
        data = f.read()

    t = time.time()
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    print(time.time() - t)

    t = time.time()
    request = predict_pb2.PredictRequest()
    request.model_spec.name = "recycle"
    request.model_spec.signature_name = "scores"
    request.inputs["image"].CopyFrom(tensor_util.make_tensor_proto([data]))
    print(time.time() - t)

    t = time.time()
    result = stub.Predict(request, 10.0)
    print(tensor_util.MakeNdarray(result.outputs["prob"]))
    print(tensor_util.MakeNdarray(result.outputs["class_id"]))
    print(time.time() - t)


if __name__ == '__main__':
    main()
