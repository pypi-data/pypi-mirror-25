# Copyright 2016 Transwarp Inc. All rights reserved.

local app = import "../../../applib/app.libsonnet";
local kube = import "../../../applib/kube.libsonnet";
local default_config = {};

function(user_config={})
  local config = default_config + user_config;
  kube.v1.Namespace(config=config)
