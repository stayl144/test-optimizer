import json, os, random, time, datetime
import boto3

s3 = boto3.client("s3")
table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
BUCKET = os.environ["BUCKET_NAME"]
BASES = ["ATL", "DTW", "MSP", "SLC"]


def handler(event, context):
    if os.environ.get("FORCE_FAIL") == "true":
        raise RuntimeError("Simulated optimizer failure")

    run_id = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    pilots = [
        {"id": f"P{i:03}", "base": random.choice(BASES),
         "fatigue_risk": round(random.random(), 2)}
        for i in range(60)
    ]
    demand = {b: random.randint(2, 6) for b in BASES}

    placements = []
    for base, need in demand.items():
        # Human-safety rule: never place a high-fatigue pilot.
        eligible = sorted(
            [p for p in pilots if p["base"] == base and p["fatigue_risk"] < 0.8],
            key=lambda p: p["fatigue_risk"],
        )
        placements += [{"base": base, "pilot": p["id"]} for p in eligible[:need]]

    result = {"run_id": run_id, "demand": demand, "placements": placements,
              "status": "PENDING_PLANNER_REVIEW"}
    s3.put_object(Bucket=BUCKET, Key=f"placements/{run_id}.json",
                  Body=json.dumps(result), ServerSideEncryption="aws:kms")
    table.put_item(Item={"run_id": run_id, "count": len(placements),
                         "status": result["status"],
                         "expires_at": int(time.time()) + 90 * 86400})
    return {"run_id": run_id, "placed": len(placements)}
