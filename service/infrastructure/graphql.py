"""Definition of the base GraphQL Query entry point."""
import graphene
from graphql.execution.base import ResolveInfo


class Query(graphene.ObjectType):
    """Query object for GraphQL API."""

    status = graphene.String()

    @staticmethod
    def resolve_status(parent, info: ResolveInfo) -> str:
        """Resolve graphql query for app status.

        Please see below for docs on resolver methods:
            https://docs.graphene-python.org/en/latest/types/
            objecttypes/#resolverimplicitstaticmethod

        Args:
            parent: Value object from the resolver of the parent field.
            info: graphql resolver info for resolving the query.

        Returns:
            Healthy message to suggest all is ok.
        """
        return 'healthy'
