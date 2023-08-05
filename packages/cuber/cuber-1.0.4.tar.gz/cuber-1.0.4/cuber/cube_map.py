from cuber import cube
from cuber import utils

class CubeMap(cube.Cube):
    def __init__(self, apply_cube_module, apply_cube_class, apply_cube_field, array_field, 
            apply_cube_params = {}, 
            disable_inmemory_cache = False, 
            disable_file_cache = False, 
            **kwargs):
        self.apply_cube_module = apply_cube_module
        self.apply_cube_class = apply_cube_class
        self.apply_cube_params = apply_cube_params
        self.apply_cube_field = apply_cube_field
        self.array_field = array_field
        self.disable_inmemory_cache = disable_inmemory_cache
        self.disable_file_cache = disable_file_cache
        self.kwargs = kwargs # data form dependency

    def name(self):
        return 'map_{}'.format(utils.universal_hash((
                self.apply_cube_module,
                self.apply_cube_class,
                self.apply_cube_params,
                self.kwargs,
            )))

    def eval(self):
        mapped = []
        module = importlib.import_module(self.apply_cube_module)
        for item in self.kwargs[self.array_field]:
            attrs = copy.deepcopy(self.apply_cube_params)
            attrs[apply_cube_field] = copy.deepcopy(item)
            cube_init = getattr(module, self.apply_cube_class)(**attrs)
            mapped_item = cube_init.get(
                    disable_inmemory_cache = self.disable_inmemory_cache,
                    disable_file_cache = self.disable_file_cache,
                )
            mapped.append(mapped_item)

        # formatting result
        result = {}
        for key, value in self.kwargs:
            if key != self.array_field:
                result[key] = value
            else: 
                result[key] = mapped
        return result
