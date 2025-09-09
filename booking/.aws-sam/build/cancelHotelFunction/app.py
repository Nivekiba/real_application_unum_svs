#from . import nosql
import boto3

dynamodb = boto3.resource("dynamodb")
hotels_table = dynamodb.Table("hotel_booking")


def lambda_handler(event, context):

    trip_id = event["trip_id"]

    # Confirm flight
    booking_id = event["booking_id"]
    hotels_table.delete_item(Key={"trip_id": trip_id, "booking_id": booking_id})

    return {"trip_id": trip_id, "status": "failure"}
