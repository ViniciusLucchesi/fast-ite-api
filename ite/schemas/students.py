def student_schema(db_item) -> dict:
    return {
        "id": str(db_item["_id"]),
        "name": db_item["name"],
        "ra": db_item["ra"],
        "email": db_item["email"],
        "course": db_item["course"],
    }

def student_list_schema(db_items) -> list[dict]:
    return [student_schema(item) for item in db_items]