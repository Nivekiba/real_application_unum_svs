import boto3


dynamodb = boto3.resource("dynamodb")
rentals_table = dynamodb.Table("car_rentals")


def lambda_handler(event, context):

    trip_id = event["trip_id"]

    # Confirm flight
    rental_id = event["rental_id"]
    rentals_table.delete_item(Key={"trip_id": trip_id, "rental_id": rental_id})

    event.pop("rental_id")
    return event
