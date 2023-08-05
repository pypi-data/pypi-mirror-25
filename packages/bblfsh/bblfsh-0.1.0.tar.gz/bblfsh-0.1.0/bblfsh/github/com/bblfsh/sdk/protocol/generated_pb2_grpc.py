# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import generated_pb2 as generated__pb2


class ProtocolServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Parse = channel.unary_unary(
        '/github.com.bblfsh.sdk.protocol.ProtocolService/Parse',
        request_serializer=generated__pb2.ParseRequest.SerializeToString,
        response_deserializer=generated__pb2.ParseResponse.FromString,
        )


class ProtocolServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Parse(self, request, context):
    """Parse uses DefaultParser to process the given parsing request to get the UAST.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ProtocolServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Parse': grpc.unary_unary_rpc_method_handler(
          servicer.Parse,
          request_deserializer=generated__pb2.ParseRequest.FromString,
          response_serializer=generated__pb2.ParseResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'github.com.bblfsh.sdk.protocol.ProtocolService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
