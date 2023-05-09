# Normal way
def en_documentEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "correct_sentence": item['correct_sentence'],
        "incorrect_sentence": item['incorrect_sentence'],
        "error_in_sentence": item["error_in_sentence"]
    }


def en_documentsEntity(entity) -> list:
    return [en_documentEntity(item) for item in entity]
# Best way


def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]
