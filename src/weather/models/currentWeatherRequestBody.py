from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

current_weather_get_swagger = swagger_auto_schema(
    method='get',
    operation_summary='Get current weather',
    operation_description='Get current weather for a specific location',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the location to get the weather for',
            required=True
        ),
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description='Authorization header with Basic Authentication',
            required=True
        ),
    ]
)

current_weather_post_swagger = swagger_auto_schema(
    method='post',
    operation_summary='Request current weather',
    operation_description='Request current weather for a specific location',
    manual_parameters=[
        openapi.Parameter(
            name='Authorization',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            description='Authorization header with Basic Authentication',
            required=True
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'location': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The name of the location to get the weather for',
                example='Sarajevo'
            ),
        },
        required=['location']
    ),
    responses={
        200: 'A successful response',
        400: 'Bad request',
        401: 'Unauthorized',
        500: 'Internal server error',
    }
)
