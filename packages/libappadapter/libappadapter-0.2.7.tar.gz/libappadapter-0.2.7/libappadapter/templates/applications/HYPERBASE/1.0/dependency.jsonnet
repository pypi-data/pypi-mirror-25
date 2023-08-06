# Copyright 2016 Transwarp Inc. All rights reserved.

local t = import "../../../applib/utils.libsonnet";
local r = import "resource.jsonnet";

function(config={})
  local appName = config.application_name;

  local appVersion = config.application_version;
  local yarnVersion = "1.0";

  local _hdfsModuleName = "hdfs";
  local _inceptorModuleName = "inceptor";
  local _yarnModuleName = "yarn";
  local _zkModuleName = "zookeeper";
  local _hyperbaseModuleName = "hyperbase";

  //-------------------
  // Dependent modules
  //-------------------

  local yarn = t.createInstance(_yarnModuleName, config, yarnVersion) +
    r.moduleResource(_yarnModuleName, config) +
    {
      dependencies: [{
        moduleName: _hdfsModuleName,
        name: _hdfsModuleName,
      }, {
        moduleName: _zkModuleName,
        name: _hdfsModuleName + "-" + _zkModuleName,
      }],
    };

  local hyperbase = t.createInstance(_hyperbaseModuleName, config, appVersion) +
    r.moduleResource(_hyperbaseModuleName, config) +
    {
      dependencies: [{
        moduleName: _hdfsModuleName,
        name: _hdfsModuleName,
      }, {
        moduleName: _yarnModuleName,
        name: appName + "-" + _yarnModuleName,
      }, {
        moduleName: _zkModuleName,
        name: _hdfsModuleName + "-" + _zkModuleName,
      }],
    };

  local TCU = {
    [_yarnModuleName]: r.moduleTCU(_yarnModuleName, config),
    [_hyperbaseModuleName]: r.moduleTCU(_hyperbaseModuleName, config),
  };

  t.getDefaultSettings(config) + {
    instance_list: [yarn, hyperbase],
    TCU: TCU,
  }
