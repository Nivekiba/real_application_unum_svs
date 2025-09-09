import uuid
import boto3

table_name = "hotel_booking"
dynamodb = boto3.resource("dynamodb")
dynamodb_table = dynamodb.Table(table_name)


def lambda_handler(event, context):

    expected_result = event["expected_result"]
    if expected_result["result"] == "failure" and expected_result["reason"] == "hotel":
        raise RuntimeError("Failed to book the hotel!")

    # We start with the hotel
    trip_id = str(uuid.uuid4().hex)
    hotel_booking_id = event["request-id"]

    # Simulate return from a service
    hotel_price = "130"
    hotel_name = "BestEver Hotel"

    dynamodb_table.put_item(
        Item={
            "trip_id": trip_id,
            "booking_id": hotel_booking_id,
            **{key: event[key] for key in event.keys() if key.startswith("hotel_")},
            "hotel_price": hotel_price,
            "hotel_name": hotel_name,
            "status": "pending",
        }
    )

    return {"trip_id": trip_id, "booking_id": hotel_booking_id, **event}
