# Copyright 2016 Transwarp Inc. All rights reserved.

# import application function library
local app = import "../../../applib/app.libsonnet";
local kube = import "../../../applib/kube.libsonnet";

local namespace = import "namespace.jsonnet";

# user-defined data
local default_config = import "config.jsonnet";

function(config={})
  local overall_config = default_config + config;
  {
    "namespace.json": namespace(overall_config),
  }
