from channels.routing import route

from plenario_exporter_s3 import consumers


channel_routing = [
    route('async-export', consumers.export),
]
