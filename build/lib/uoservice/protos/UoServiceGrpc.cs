// <auto-generated>
//     Generated by the protocol buffer compiler.  DO NOT EDIT!
//     source: UoService.proto
// </auto-generated>
#pragma warning disable 0414, 1591
#region Designer generated code

using grpc = global::Grpc.Core;

namespace Uoservice {
  public static partial class UoService
  {
    static readonly string __ServiceName = "uoservice.UoService";

    static readonly grpc::Marshaller<global::Uoservice.Config> __Marshaller_uoservice_Config = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::Uoservice.Config.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::Uoservice.States> __Marshaller_uoservice_States = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::Uoservice.States.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::Uoservice.Actions> __Marshaller_uoservice_Actions = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::Uoservice.Actions.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::Uoservice.Empty> __Marshaller_uoservice_Empty = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::Uoservice.Empty.Parser.ParseFrom);
    static readonly grpc::Marshaller<global::Uoservice.SemaphoreAction> __Marshaller_uoservice_SemaphoreAction = grpc::Marshallers.Create((arg) => global::Google.Protobuf.MessageExtensions.ToByteArray(arg), global::Uoservice.SemaphoreAction.Parser.ParseFrom);

    static readonly grpc::Method<global::Uoservice.Config, global::Uoservice.States> __Method_Reset = new grpc::Method<global::Uoservice.Config, global::Uoservice.States>(
        grpc::MethodType.Unary,
        __ServiceName,
        "Reset",
        __Marshaller_uoservice_Config,
        __Marshaller_uoservice_States);

    static readonly grpc::Method<global::Uoservice.Config, global::Uoservice.States> __Method_ReadObs = new grpc::Method<global::Uoservice.Config, global::Uoservice.States>(
        grpc::MethodType.Unary,
        __ServiceName,
        "ReadObs",
        __Marshaller_uoservice_Config,
        __Marshaller_uoservice_States);

    static readonly grpc::Method<global::Uoservice.Actions, global::Uoservice.Empty> __Method_WriteAct = new grpc::Method<global::Uoservice.Actions, global::Uoservice.Empty>(
        grpc::MethodType.Unary,
        __ServiceName,
        "WriteAct",
        __Marshaller_uoservice_Actions,
        __Marshaller_uoservice_Empty);

    static readonly grpc::Method<global::Uoservice.SemaphoreAction, global::Uoservice.Empty> __Method_ActSemaphoreControl = new grpc::Method<global::Uoservice.SemaphoreAction, global::Uoservice.Empty>(
        grpc::MethodType.Unary,
        __ServiceName,
        "ActSemaphoreControl",
        __Marshaller_uoservice_SemaphoreAction,
        __Marshaller_uoservice_Empty);

    static readonly grpc::Method<global::Uoservice.SemaphoreAction, global::Uoservice.Empty> __Method_ObsSemaphoreControl = new grpc::Method<global::Uoservice.SemaphoreAction, global::Uoservice.Empty>(
        grpc::MethodType.Unary,
        __ServiceName,
        "ObsSemaphoreControl",
        __Marshaller_uoservice_SemaphoreAction,
        __Marshaller_uoservice_Empty);

    static readonly grpc::Method<global::Uoservice.Config, global::Uoservice.States> __Method_ReadReplay = new grpc::Method<global::Uoservice.Config, global::Uoservice.States>(
        grpc::MethodType.Unary,
        __ServiceName,
        "ReadReplay",
        __Marshaller_uoservice_Config,
        __Marshaller_uoservice_States);

    static readonly grpc::Method<global::Uoservice.Config, global::Uoservice.Empty> __Method_ReadMPQFile = new grpc::Method<global::Uoservice.Config, global::Uoservice.Empty>(
        grpc::MethodType.Unary,
        __ServiceName,
        "ReadMPQFile",
        __Marshaller_uoservice_Config,
        __Marshaller_uoservice_Empty);

    /// <summary>Service descriptor</summary>
    public static global::Google.Protobuf.Reflection.ServiceDescriptor Descriptor
    {
      get { return global::Uoservice.UoServiceReflection.Descriptor.Services[0]; }
    }

    /// <summary>Base class for server-side implementations of UoService</summary>
    public abstract partial class UoServiceBase
    {
      public virtual global::System.Threading.Tasks.Task<global::Uoservice.States> Reset(global::Uoservice.Config request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      public virtual global::System.Threading.Tasks.Task<global::Uoservice.States> ReadObs(global::Uoservice.Config request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      public virtual global::System.Threading.Tasks.Task<global::Uoservice.Empty> WriteAct(global::Uoservice.Actions request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      public virtual global::System.Threading.Tasks.Task<global::Uoservice.Empty> ActSemaphoreControl(global::Uoservice.SemaphoreAction request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      public virtual global::System.Threading.Tasks.Task<global::Uoservice.Empty> ObsSemaphoreControl(global::Uoservice.SemaphoreAction request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      public virtual global::System.Threading.Tasks.Task<global::Uoservice.States> ReadReplay(global::Uoservice.Config request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

      public virtual global::System.Threading.Tasks.Task<global::Uoservice.Empty> ReadMPQFile(global::Uoservice.Config request, grpc::ServerCallContext context)
      {
        throw new grpc::RpcException(new grpc::Status(grpc::StatusCode.Unimplemented, ""));
      }

    }

    /// <summary>Client for UoService</summary>
    public partial class UoServiceClient : grpc::ClientBase<UoServiceClient>
    {
      /// <summary>Creates a new client for UoService</summary>
      /// <param name="channel">The channel to use to make remote calls.</param>
      public UoServiceClient(grpc::Channel channel) : base(channel)
      {
      }
      /// <summary>Creates a new client for UoService that uses a custom <c>CallInvoker</c>.</summary>
      /// <param name="callInvoker">The callInvoker to use to make remote calls.</param>
      public UoServiceClient(grpc::CallInvoker callInvoker) : base(callInvoker)
      {
      }
      /// <summary>Protected parameterless constructor to allow creation of test doubles.</summary>
      protected UoServiceClient() : base()
      {
      }
      /// <summary>Protected constructor to allow creation of configured clients.</summary>
      /// <param name="configuration">The client configuration.</param>
      protected UoServiceClient(ClientBaseConfiguration configuration) : base(configuration)
      {
      }

      public virtual global::Uoservice.States Reset(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return Reset(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.States Reset(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_Reset, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.States> ResetAsync(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ResetAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.States> ResetAsync(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_Reset, null, options, request);
      }
      public virtual global::Uoservice.States ReadObs(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReadObs(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.States ReadObs(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_ReadObs, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.States> ReadObsAsync(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReadObsAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.States> ReadObsAsync(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_ReadObs, null, options, request);
      }
      public virtual global::Uoservice.Empty WriteAct(global::Uoservice.Actions request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return WriteAct(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.Empty WriteAct(global::Uoservice.Actions request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_WriteAct, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> WriteActAsync(global::Uoservice.Actions request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return WriteActAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> WriteActAsync(global::Uoservice.Actions request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_WriteAct, null, options, request);
      }
      public virtual global::Uoservice.Empty ActSemaphoreControl(global::Uoservice.SemaphoreAction request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ActSemaphoreControl(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.Empty ActSemaphoreControl(global::Uoservice.SemaphoreAction request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_ActSemaphoreControl, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> ActSemaphoreControlAsync(global::Uoservice.SemaphoreAction request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ActSemaphoreControlAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> ActSemaphoreControlAsync(global::Uoservice.SemaphoreAction request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_ActSemaphoreControl, null, options, request);
      }
      public virtual global::Uoservice.Empty ObsSemaphoreControl(global::Uoservice.SemaphoreAction request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ObsSemaphoreControl(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.Empty ObsSemaphoreControl(global::Uoservice.SemaphoreAction request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_ObsSemaphoreControl, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> ObsSemaphoreControlAsync(global::Uoservice.SemaphoreAction request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ObsSemaphoreControlAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> ObsSemaphoreControlAsync(global::Uoservice.SemaphoreAction request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_ObsSemaphoreControl, null, options, request);
      }
      public virtual global::Uoservice.States ReadReplay(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReadReplay(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.States ReadReplay(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_ReadReplay, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.States> ReadReplayAsync(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReadReplayAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.States> ReadReplayAsync(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_ReadReplay, null, options, request);
      }
      public virtual global::Uoservice.Empty ReadMPQFile(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReadMPQFile(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual global::Uoservice.Empty ReadMPQFile(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.BlockingUnaryCall(__Method_ReadMPQFile, null, options, request);
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> ReadMPQFileAsync(global::Uoservice.Config request, grpc::Metadata headers = null, global::System.DateTime? deadline = null, global::System.Threading.CancellationToken cancellationToken = default(global::System.Threading.CancellationToken))
      {
        return ReadMPQFileAsync(request, new grpc::CallOptions(headers, deadline, cancellationToken));
      }
      public virtual grpc::AsyncUnaryCall<global::Uoservice.Empty> ReadMPQFileAsync(global::Uoservice.Config request, grpc::CallOptions options)
      {
        return CallInvoker.AsyncUnaryCall(__Method_ReadMPQFile, null, options, request);
      }
      /// <summary>Creates a new instance of client from given <c>ClientBaseConfiguration</c>.</summary>
      protected override UoServiceClient NewInstance(ClientBaseConfiguration configuration)
      {
        return new UoServiceClient(configuration);
      }
    }

    /// <summary>Creates service definition that can be registered with a server</summary>
    /// <param name="serviceImpl">An object implementing the server-side handling logic.</param>
    public static grpc::ServerServiceDefinition BindService(UoServiceBase serviceImpl)
    {
      return grpc::ServerServiceDefinition.CreateBuilder()
          .AddMethod(__Method_Reset, serviceImpl.Reset)
          .AddMethod(__Method_ReadObs, serviceImpl.ReadObs)
          .AddMethod(__Method_WriteAct, serviceImpl.WriteAct)
          .AddMethod(__Method_ActSemaphoreControl, serviceImpl.ActSemaphoreControl)
          .AddMethod(__Method_ObsSemaphoreControl, serviceImpl.ObsSemaphoreControl)
          .AddMethod(__Method_ReadReplay, serviceImpl.ReadReplay)
          .AddMethod(__Method_ReadMPQFile, serviceImpl.ReadMPQFile).Build();
    }

  }
}
#endregion