import graphene

import tagiot.schema


class Query(tagiot.schema.Query, graphene.ObjectType):
    pass

class Mutation(tagiot.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

# End of ./schema.py
