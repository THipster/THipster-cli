import os
import importlib


def get_thipster_class(
    parent_module_name: str,
    module_name: str,
    class_name_extension: str,
) -> type:
    module = importlib.import_module(
        f'thipster.{parent_module_name.lower()}.{module_name.lower()}',
    )
    return getattr(
        module,
        (module_name.capitalize() if module_name.islower() else module_name) +
        class_name_extension,
    )


def check_thipster_module_exists(parent_module_name: str, module_name: str) -> bool:
    try:
        importlib.import_module(
            f'thipster.{parent_module_name.lower()}.{module_name.lower()}',
        )
        return True
    except ModuleNotFoundError:
        return False


def get_thipster_module_class_list(module_name: str) -> list[str]:
    # return list of classes in module
    module = importlib.import_module(
        f'thipster.{module_name.lower()}',
    )
    module_class_list = []
    with os.scandir(os.path.dirname(module.__file__)) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.py') and not \
                    entry.name.startswith('__'):
                module_class = entry.name.capitalize() if entry.name.islower() else \
                    entry.name
                module_class_list.append(module_class)
    return module_class_list


def get_auth_provider_class(provider: str) -> type:
    return get_thipster_class('auth', provider, 'Auth')
