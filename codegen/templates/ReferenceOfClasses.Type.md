{% if type.name != "void" %}: {% if type.cardinality == "iterator" %}iterator of {% endif %}{% if type.cardinality == "list" %}list of {% endif %}{% if type.cardinality == "dict" %}dict of {{ type.key_name }} to {% endif %}{% if not type.simple %}`{% endif %}{% if type.name == "datetime" %}datetime.datetime{% else %}{{ type.name }}{% endif %}{% if not type.simple %}`{% endif %}{% endif %}