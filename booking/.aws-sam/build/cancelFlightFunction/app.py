#from . import nosql
import boto3

dynamodb = boto3.resource("dynamodb")
flights_table = dynamodb.Table("flights")


def lambda_handler(event, context):

    trip_id = event["trip_id"]

    # Confirm flight
    flight_id = event["flight_id"]
    flights_table.delete_item(Key={"trip_id": trip_id, "flight_id": flight_id})

    event.pop("flight_id")
    return event
