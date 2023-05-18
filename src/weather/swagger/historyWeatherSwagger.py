from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Swagger documentation for Get Historical Data for Weather endpoint
history_weather_get_swagger = swagger_auto_schema(
    method='get',
    operation_summary='Get historical data for weather',
    operation_description='Get historical weather data for a specific location for a range of dates',
    manual_parameters=[
        openapi.Parameter(
            name='location',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The name of the location to get the weather for',
            example="Sarajevo",
            required=True
        ),
        openapi.Parameter(
            name='start_date',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The start date for historical data (YYYY-MM-DD)',
            example="2022-01-01",
            required=True
        ),
        openapi.Parameter(
            name='end_date',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='The end date for historical data (YYYY-MM-DD)',
            example="2022-01-05",
            required=True
        ),
    ]
)

# Swagger documentation for Create Historical Data for Weather Entry endpoint
history_weather_post_swagger = swagger_auto_schema(
    method='post',
    operation_summary='Create historical data for weather entry',
    operation_description='Create a historical weather data for a specific location and range of dates',
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
                example="Sarajevo"
            ),
            'start_date': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Start date (YYYY-MM-DD)',
                example='2023-01-01'
            ),
            'end_date': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='End date (YYYY-MM-DD)',
                example='2023-01-05'
            )
        },
        required=['location', 'start_date', 'end_date']
    ),
    responses={
        200: 'A successful response',
        400: 'Bad request',
        401: 'Unauthorized',
        500: 'Internal server error',
    }
)
