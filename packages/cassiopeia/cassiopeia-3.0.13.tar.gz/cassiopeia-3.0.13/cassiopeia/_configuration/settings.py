from typing import TypeVar, Type, Dict, Union, Optional
import logging
import importlib

from datapipelines import DataPipeline

from ..data import Region, Platform

T = TypeVar("T")

logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)


def create_pipeline(service_configs: Dict, verbose: bool = False) -> DataPipeline:
    transformers = []

    # Always use the Riot API transformers
    from ..transformers import __transformers__ as riotapi_transformer
    transformers.extend(riotapi_transformer)

    # Add sources / sinks by name from config
    # TODO Add expirations
    services = []
    for store_name, config in service_configs.items():
        package = config.pop("package", None)
        if package is None:
            package = "cassiopeia.datastores"
        module = importlib.import_module(name=package)
        store_cls = getattr(module, store_name)
        store = store_cls(**config)
        services.append(store)
        service_transformers = getattr(module, "__transformers__", [])
        transformers.extend(service_transformers)

    pipeline = DataPipeline(services, transformers)

    # Manually put the cache on the pipeline.
    from ..datastores import Cache
    for datastore in services:
        if isinstance(datastore, Cache):
            pipeline._cache = datastore
            break
    else:
        pipeline._cache = None

    if verbose:
        for service in services:
            print("Service:", service)
            for p in service.provides:
                print("  Provides:", p)
        for transformer in transformers:
            for t in transformer.transforms.items():
                print("Transformer:", t)
        print()

    return pipeline


class Settings(object):
    def __init__(self, settings):
        globals_ = settings.get("global", {})
        self.__version_from_match = globals_.get("version_from_match", "patch")  # Valid json values are: "version", "patch", and null
        self.__default_region = globals_.get("default_region", None)
        if self.__default_region is not None:
            self.__default_region = Region(self.__default_region.upper())

        self.__plugins = settings.get("plugins", {})

        self.__pipeline_args = settings.get("pipeline", {"Cache": {}, "DDragon": {}, "RiotAPI": {"api_key": "RIOT_API_KEY"}})
        self.__pipeline = None  # type: DataPipeline

        logging_config = settings.get("logging", {})
        self.__default_print_calls = logging_config.get("print_calls", True)
        self.__default_print_riot_api_key = logging_config.get("print_riot_api_key", False)
        for name in ["default", "core"]:
            logger = logging.getLogger(name)
            level = logging_config.get(name, logging.WARNING)
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

    def set_region(self, region: Union[Region, str]):
        if isinstance(region, str):
            region = Region(region.upper())
        self.__default_region = region

    @property
    def pipeline(self) -> DataPipeline:
        if self.__pipeline is None:
            self.__pipeline = create_pipeline(verbose=False, service_configs=self.__pipeline_args)
        return self.__pipeline

    @property
    def default_region(self):
        return self.__default_region

    @property
    def default_platform(self):
        return Platform[self.__default_region.name]

    @property
    def version_from_match(self):
        return self.__version_from_match

    @property
    def plugins(self):
        return self.__plugins

    def set_riot_api_key(self, key):
        from ..datastores.riotapi import RiotAPI
        for sources in self.pipeline._sources:
            for source in sources:
                if isinstance(source, RiotAPI):
                    source.set_api_key(key)

    def clear_sinks(self, name: Optional[str] = None, type: Type[T] = None):
        types = {type}
        if type is not None:
            from ..core.common import CoreData, CassiopeiaObject
            if issubclass(type, CassiopeiaObject):
                for t in type._data_types:
                    types.add(t)
                    types.add(t._dto_type)
            elif issubclass(type, CoreData):
                types.add(type._dto_type)

        for sink in self.pipeline._sinks:
            if name is None or sink.__class__.__name__ == name:
                for type in types:
                    sink.clear(type)
