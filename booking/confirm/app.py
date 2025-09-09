#from . import nosql
import boto3

dynamodb = boto3.resource("dynamodb")
flights_table = dynamodb.Table("flights")
rentals_table = dynamodb.Table("car_rentals")
hotels_table = dynamodb.Table("hotel_booking")


def lambda_handler(event, context):

    expected_result = event["expected_result"]
    if expected_result["result"] == "failure" and expected_result["reason"] == "confirm":
        raise RuntimeError("Failed to confirm the booking!")

    trip_id = event["trip_id"]

    # Confirm flight
    flight_id = event["flight_id"]
    flights_table.update_item(
        Key={"trip_id": trip_id, "flight_id": flight_id},
        UpdateExpression="SET #S = :s",
        ExpressionAttributeNames={"#S": "status"},
        ExpressionAttributeValues={":s": "booked"},
    )

    # Confirm car rental
    rentals_table.update_item(
        Key={"trip_id": trip_id, "rental_id": event["rental_id"]},
        UpdateExpression="SET #S = :s",
        ExpressionAttributeNames={"#S": "status"},
        ExpressionAttributeValues={":s": "booked"},
    )

    # Confirm hotel booking
    hotels_table.update_item(
        Key={"trip_id": trip_id, "booking_id": event["booking_id"]},
        UpdateExpression="SET #S = :s",
        ExpressionAttributeNames={"#S": "status"},
        ExpressionAttributeValues={":s": "booked"},
    )

    return {
        "trip_id": trip_id,
        "status": "success",
        "flight_id": flight_id,
        "rental_id": event["rental_id"],
        "booking_id": event["booking_id"],
    }
