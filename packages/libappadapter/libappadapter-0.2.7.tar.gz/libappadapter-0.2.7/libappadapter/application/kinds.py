# Copyright 2017 Transwarp Inc. All rights reserved.
from libappadapter.application.app_config import APPLICATION_TEMPLATES


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

# Registry of supported applications
AppType = Enum([i.upper() for i in APPLICATION_TEMPLATES.keys()])
