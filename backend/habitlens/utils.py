"""Helper functions for HabitLens."""


def extract_property_value(prop):
    """Helper to safely extract a Notion property value."""
    if prop is None:
        return None

    if "checkbox" in prop:
        return prop["checkbox"]
    if "select" in prop and prop["select"]:
        return prop["select"]["name"]
    if "multi_select" in prop and prop["multi_select"]:
        return [tag["name"] for tag in prop["multi_select"]]
    if "number" in prop:
        return prop["number"]
    if "date" in prop and prop["date"]:
        return prop["date"]["start"]
    if "rich_text" in prop and prop["rich_text"]:
        return prop["rich_text"][0]["plain_text"]

    return None
