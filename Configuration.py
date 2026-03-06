import dataclasses
@dataclasses.dataclass
class Configuration:
    pth_to_raw_dataset: str
    pth_to_refmap: str
    pth_to_endpoint_root: str
    pth_to_pusher_batch_abs: str
    interval: float

_DEFAULT_CONFIGURATION = Configuration(
    pth_to_raw_dataset="../shit_transfer/stats/dataset.bin",
    pth_to_refmap="../shit_transfer/stats/meta-id-refmap",
    pth_to_endpoint_root="../SHIT-preprints-metrics-history/src",
    pth_to_pusher_batch_abs="D:/meow/SHIT-preprints-metrics-history/pusher.cmd",
    interval=60*60,
)