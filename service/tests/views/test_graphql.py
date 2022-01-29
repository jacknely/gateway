"""Base tests for the graphql endpoint."""
import json


def test_base_graphql(app):
    """Tests the base graphql service is running correctly."""
    response = app.post(
        path='/graphql',
        data={'query': '{ status }'}
    )

    assert response.status_code == 200
    assert json.loads(response.data) == {
        'data': {
            'status': 'healthy'
        }
    }
