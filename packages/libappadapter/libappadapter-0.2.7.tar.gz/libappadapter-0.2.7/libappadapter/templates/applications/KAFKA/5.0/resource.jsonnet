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
      kafka: {
        kafka_tmp_storage: {
          storageClass: s.StorageClass,
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
          size: s.DiskTmpSize,
          accessMode: "ReadWriteOnce",
        },
        kafka_storage_config: {
          storageClass: s.StorageClass,
          size: s.DiskDataSize,
          accessModes: ["ReadWriteOnce"],
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
        },
      },
      zookeeper: {
        zk_storage_config: {
          storageClass: s.StorageClass,
          size: s.DiskNormalSize,
          accessModes: ["ReadWriteOnce"],
          limits: {
            "blkio.throttle.read_iops_device": s.ReadIOPS,
            "blkio.throttle.write_iops_device": s.WriteIOPS,
          },
        },
      },
    };

    local resource = {
      kafka:
        if Debug_Request then
          {
            kafka_cpu_limit: 0.4,
            kafka_memory_limit: 1,
            kafka_cpu_request: self.kafka_cpu_limit,
            kafka_memory_request: self.kafka_memory_limit,
          }
        else
          {
            kafka_cpu_limit: t.objectField(config, "kafka_cpu_limit", 1),
            kafka_memory_limit: t.objectField(config, "kafka_memory_limit", 2),
            kafka_cpu_request: t.objectField(config, "kafka_cpu_request", self.kafka_cpu_limit),
            kafka_memory_request: t.objectField(config, "kafka_memory_request", self.kafka_memory_limit),
          },
      zookeeper:
        if Debug_Request then
          {
            zk_cpu_limit: 0.4,
            zk_memory_limit: 1,
            zk_cpu_request: self.zk_cpu_limit,
            zk_memory_request: self.zk_memory_limit,
          }
        else
          {
            // Use namenode as the achor point
            local cpu_limit = resource.kafka.kafka_cpu_limit,
            local memory_limit = resource.kafka.kafka_memory_limit,

            zk_cpu_limit: t.objectField(config, "zk_cpu_limit", t.raRange(cpu_limit * 0.5, min=1, max=cpu_limit)),
            zk_memory_limit: t.objectField(config, "zk_memory_limit", t.raRange(memory_limit * 0.5, min=1, max=memory_limit)),
            zk_cpu_request: t.objectField(config, "zk_cpu_request", self.zk_cpu_limit),
            zk_memory_request: t.objectField(config, "zk_memory_request", self.zk_memory_limit),
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
      kafka: [
        "kafka_cpu_limit",
      ],
      zookeeper: [
        "zk_cpu_limit",
      ],
    };

    local mem_metrics = {
      kafka: [
        "kafka_memory_limit",
      ],
      zookeeper: [
        "zk_memory_limit",
      ],
    };

    local ssd_metrics = {};

    local disk_metrics = {};

    local unifiedConfig = t.getUnifiedInstanceSettings(config);
    t.calculateModuleTCU(moduleName, unifiedConfig, $.__moduleResourceRaw,
      cpu_metrics, mem_metrics, ssd_metrics, disk_metrics),
}
