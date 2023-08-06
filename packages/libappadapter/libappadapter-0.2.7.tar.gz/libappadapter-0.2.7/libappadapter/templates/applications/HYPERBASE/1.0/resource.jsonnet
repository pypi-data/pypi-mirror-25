# Copyright 2016 Transwarp Inc. All rights reserved.

local t = import "../../../applib/utils.libsonnet";

{
  /*
   * Define resource metrics for each module
   */
  __moduleResourceRaw(moduleName, config={})::
    local Debug_Request = t.objectField(config, "Develop", false);

    local s = t.extractStorageParams(config);

    local storage = {
      yarn: {
        yarn_resourcemanager_tmp_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskTmpSize,
          accessMode: "ReadWriteOnce",
        },
        yarn_secondary_tmp_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskTmpSize,
          accessMode: "ReadWriteOnce",
        },
        yarn_nodemanager_tmp_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskTmpSize,
          accessMode: "ReadWriteOnce",
        },
        yarn_nodemanager_data_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskDataSize,
          accessMode: "ReadWriteOnce",
        },
        yarn_timelineserver_tmp_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskTmpSize,
          accessMode: "ReadWriteOnce",
        },
        yarn_historyserver_tmp_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskTmpSize,
          accessMode: "ReadWriteOnce",
        },
      },
      hyperbase: {},
    };

    local resource = {
      yarn:
        if Debug_Request then
          {
            yarn_cpu_limit: 0.5,
            yarn_memory_limit: 1,
            yarn_cpu_request: self.yarn_cpu_limit,
            yarn_memory_request: self.yarn_memory_limit,
          }
        else
          {
            yarn_cpu_limit: t.objectField(config, "yarn_cpu_limit", 2),
            yarn_memory_limit: t.objectField(config, "yarn_memory_limit", 4),
            yarn_cpu_request: t.objectField(config, "yarn_cpu_request", self.yarn_cpu_limit),
            yarn_memory_request: t.objectField(config, "yarn_memory_request", self.yarn_memory_limit),
          },
      hyperbase:
        if Debug_Request then
          {
            hbase_master_cpu_limit: 0.5,
            hbase_master_memory_limit: 1,
            hbase_master_cpu_request: self.hbase_master_cpu_limit,
            hbase_master_memory_request: self.hbase_master_memory_limit,

            hbase_rs_cpu_limit: 0.5,
            hbase_rs_memory_limit: 1,
            hbase_rs_cpu_request: self.hbase_rs_cpu_limit,
            hbase_rs_memory_request: self.hbase_rs_memory_limit,

            hbase_rest_cpu_limit: 0.5,
            hbase_rest_memory_limit: 1,
            hbase_rest_cpu_request: self.hbase_rest_cpu_limit,
            hbase_rest_memory_request: self.hbase_rest_memory_limit,

            hbase_thrift_cpu_limit: 0.5,
            hbase_thrift_memory_limit: 1,
            hbase_thrift_cpu_request: self.hbase_thrift_cpu_limit,
            hbase_thrift_memory_request: self.hbase_thrift_memory_limit,
          }
        else
          {
            hbase_master_cpu_limit: t.objectField(config, "hbase_master_cpu_limit", 4),
            hbase_master_memory_limit: t.objectField(config, "hbase_master_memory_limit", 4),
            hbase_master_cpu_request: t.objectField(config, "hbase_master_cpu_request", self.hbase_master_cpu_limit),
            hbase_master_memory_request: t.objectField(config, "hbase_master_memory_request", self.hbase_master_memory_limit),

            hbase_rs_cpu_limit: t.objectField(config, "hbase_rs_cpu_limit", 2),
            hbase_rs_memory_limit: t.objectField(config, "hbase_rs_memory_limit", 1),
            hbase_rs_cpu_request: t.objectField(config, "hbase_rs_cpu_request", self.hbase_rs_cpu_limit),
            hbase_rs_memory_request: t.objectField(config, "hbase_rs_memory_request", self.hbase_rs_memory_limit),

            // Use namenode as the achor point in dynamic resource distribution
            local cpu_limit = self.hbase_rs_cpu_limit,
            local memory_limit = self.hbase_rs_memory_limit,

            hbase_rest_cpu_limit: t.objectField(config, "hbase_rest_cpu_limit", t.raRange(cpu_limit * 0.5, min=1, max=cpu_limit)),
            hbase_rest_memory_limit: t.objectField(config, "hbase_rest_memory_limit", t.raRange(memory_limit * 0.5, min=1, max=memory_limit)),
            hbase_rest_cpu_request: t.objectField(config, "hbase_rest_cpu_request", self.hbase_rest_cpu_limit),
            hbase_rest_memory_request: t.objectField(config, "hbase_rest_memory_request", self.hbase_rest_memory_limit),

            hbase_thrift_cpu_limit: t.objectField(config, "hbase_thrift_cpu_limit", t.raRange(cpu_limit * 0.5, min=1, max=cpu_limit)),
            hbase_thrift_memory_limit: t.objectField(config, "hbase_thrift_memory_limit", t.raRange(memory_limit * 0.5, min=1, max=memory_limit)),
            hbase_thrift_cpu_request: t.objectField(config, "hbase_thrift_cpu_request", self.hbase_thrift_cpu_limit),
            hbase_thrift_memory_request: t.objectField(config, "hbase_thrift_memory_request", self.hbase_thrift_memory_limit),
          },
    };
    // Return storage and resource specification
    {
      storage: if std.objectHas(storage, moduleName) then storage[moduleName] else {},
      resource: if std.objectHas(resource, moduleName) then resource[moduleName] else {},
    },

  /*
   * Get resurce configs for each module
   */
  moduleResource(moduleName, config={})::
    local unifiedConfig = t.getUnifiedInstanceSettings(config);
    local module = $.__moduleResourceRaw(moduleName, unifiedConfig);
    {
      configs: module.resource + module.storage,
    },

  /*
   * Define TCU calculation for each module
   */
  moduleTCU(moduleName, config={})::
    local cpu_metrics = {
      hyperbase: [
        "hbase_master_cpu_limit",
        "hbase_rs_cpu_limit",
        "hbase_rest_cpu_limit",
        "hbase_thrift_cpu_limit",
      ],
      yarn: [
        "yarn_cpu_limit",
      ],
    };

    local mem_metrics = {
      hyperbase: [
        "hbase_master_memory_limit",
        "hbase_rs_memory_limit",
        "hbase_rest_memory_limit",
        "hbase_thrift_memory_limit",
      ],
      yarn: [
        "yarn_memory_limit",
      ],
    };

    local ssd_metrics = {

    };

    local disk_metrics = {

    };

    local unifiedConfig = t.getUnifiedInstanceSettings(config);
    t.calculateModuleTCU(moduleName, unifiedConfig, $.__moduleResourceRaw,
      cpu_metrics, mem_metrics, ssd_metrics, disk_metrics),
}
