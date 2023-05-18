from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Swagger documentation for Get Forecast Weather endpoint
forecast_weather_get_swagger = swagger_auto_schema(
    method='get',
    operation_summary='Get forecast weather',
    operation_description='Get forecast weather for a specific location',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the location to get the weather for',
            required=True
        ),
        openapi.Parameter(
            name='days',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description='The number of days to get the weather for',
            required=True
        ),
    ]
)

# Swagger documentation for Create Forecast Weather Entry endpoint
forecast_weather_post_swagger = swagger_auto_schema(
    method='post',
    operation_summary='Create forecast weather entry',
    operation_description='Create a forecast weather entry for a specific location and number of days',
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
                description='The name of the location',
                example='Sarajevo'
            ),
            'days': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='Number of days for location',
                example='5'
            )
        },
        required=['location', 'days']
    ),
    responses={
        200: 'A successful response',
        400: 'Bad request',
        401: 'Unauthorized',
        500: 'Internal server error',
    }
)
