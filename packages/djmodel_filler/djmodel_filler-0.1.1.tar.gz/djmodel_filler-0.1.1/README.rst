**djmodel_filler**

built with the purpose of hiding the django model filling process,
with data which went through the mapping of deep_mapper


initialize with django model

``mf = ModelFiller(model)``

use xmlparser for local xml file, or provide your own data for mapping

``data = xmlparser('test_source.xml')``

start the data transfer thru the mapper

``mf.transfer_data(data, MAP_STRUCTURE, '/feed/events/event')``

at the end - your model will got new entities that created from data parts
for mapping process info please check `deep_mapper <http://github.com/gebriallairbeg/deep_mapper>`_


available from pip:

``pip install djmodel_filler``