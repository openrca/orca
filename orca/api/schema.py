from marshmallow import Schema, fields


class GraphObjectSchema(Schema):

    id = fields.String()


class PropertiesSchema(Schema):

    name = fields.String()
    namespace = fields.String()


class NodeSchema(GraphObjectSchema):

    origin = fields.String()
    kind = fields.String()
    properties = fields.Nested(PropertiesSchema())


class DetailedNodeSchema(NodeSchema):

    properties = fields.Raw()


class LinkSchema(GraphObjectSchema):

    source = fields.String(attribute='source.id')
    target = fields.String(attribute='target.id')


class GraphSchema(Schema):

    nodes = fields.List(fields.Nested(DetailedNodeSchema()))
    links = fields.List(fields.Nested(LinkSchema()))


class GraphQuerySchema(Schema):

    time_point = fields.Integer(missing=None)


class AlertSchema(Schema):

    id = fields.String()
    origin = fields.String()
    name = fields.String(attribute='properties.name')
    message = fields.String(attribute='properties.message')
    severity = fields.String(attribute='properties.severity')
    source = fields.Nested(NodeSchema(), attribute='properties.source_mapping')
    created_at = fields.String()
    updated_at = fields.String()
