import graphene

import tagiot.schema


class Query(tagiot.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)

# End of ./schema.py
