from deep_mapper import process_mapping


class ModelFiller(object):

    def __init__(self, model):
        self.model = model

    def transfer_data(self, data, map_options, map_root_path):
        '''
        method helper that provide filling Django model with objects
        that was ejected from data through map_options & map_root_path
        '''
        mapped_data = process_mapping(
            data, map_options, map_root_path) if map_options else data
        for item in mapped_data:
            self.model.objects.create(**item)