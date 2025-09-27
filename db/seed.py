# db/seed.py
import sys, json
from db.client import connect

def seed_form(json_path: str):
    client = connect()
    forms = client.collections.use("Form")
    fields = client.collections.use("FormField")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Insert form
    form_id = forms.data.insert({"name": data["name"]})
    print(f"✅ Inserted form: {data['name']}")

    # Insert fields
    with fields.batch.dynamic() as b:
        for field in data["fields"]:
            b.add_object(
                {"key": field["key"], "label": field["label"]},
                references={"ofForm": form_id}
            )
    print("✅ Fields inserted.")
    client.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db/seed.py data/form.json")
        sys.exit(1)
    seed_form(sys.argv[1])
