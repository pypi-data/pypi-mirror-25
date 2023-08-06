# Copyright 2016 Transwarp Inc. All rights reserved.

local t = import "../../../applib/utils.libsonnet";
local r = import "resource.jsonnet";

function(config={})
  local appName = config.application_name;

  local appVersion = config.application_version;

  local _hdfsModuleName = "hdfs";
  local _yarnModuleName = "yarn";
  local _sophonModuleName = "sophon";

  //-------------------
  // Dependent modules
  //-------------------

  local sophon = t.createInstance(_sophonModuleName, config, appVersion) +
    r.moduleResource(_sophonModuleName, config) +
    {
      dependencies: [{
        moduleName: _hdfsModuleName,
        name: _hdfsModuleName,
      }, {
        moduleName: _yarnModuleName,
        name: _yarnModuleName,
      }],
    };

  t.getDefaultSettings(config) + {
    instance_list: [sophon],
    TCU: {
      [_sophonModuleName]: r.moduleTCU(_sophonModuleName, config),
    },
  }
