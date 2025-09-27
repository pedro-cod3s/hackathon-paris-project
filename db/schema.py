# db/schema.py
from db.client import connect
from weaviate.classes import config as wc

client = connect()

# Drop old schema (dev only)
for name in ["Answer", "Utterance", "Conversation", "FormField", "Form"]:
    try:
        client.collections.delete(name)
    except Exception:
        pass

Form = client.collections.create(
    name="Form",
    properties=[wc.Property(name="name", data_type=wc.DataType.TEXT)],
    vector_config=wc.Configure.Vectors.text2vec_openai()
)

FormField = client.collections.create(
    name="FormField",
    properties=[
        wc.Property(name="key", data_type=wc.DataType.TEXT),
        wc.Property(name="label", data_type=wc.DataType.TEXT)
    ],
    references=[wc.ReferenceProperty(name="ofForm", target_collection="Form")],
    vector_config=wc.Configure.Vectors.text2vec_openai()
)

Conversation = client.collections.create(
    name="Conversation",
    properties=[wc.Property(name="user_id", data_type=wc.DataType.TEXT),
                wc.Property(name="status", data_type=wc.DataType.TEXT, index_filterable=True),
                wc.Property(name="safety_flag", data_type=wc.DataType.TEXT, index_filterable=True)],
    references=[wc.ReferenceProperty(name="form", target_collection="Form")],
    vector_config=wc.Configure.Vectors.text2vec_openai(vectorize_collection_name=False)
)

Utterance = client.collections.create(
    name="Utterance",
    properties=[
        wc.Property(name="role", data_type=wc.DataType.TEXT),
        wc.Property(name="text", data_type=wc.DataType.TEXT),
        wc.Property(name="summary", data_type=wc.DataType.TEXT),
        wc.Property(name="emotion_text", data_type=wc.DataType.TEXT, index_filterable=True),
        wc.Property(name="red_flags", data_type=wc.DataType.TEXT_ARRAY, index_filterable=True),
        wc.Property(name="facts_json", data_type=wc.DataType.OBJECT),
        wc.Property(name="missing_after_turn", data_type=wc.DataType.TEXT_ARRAY, index_filterable=True),
    ],
    references=[
        wc.ReferenceProperty(name="conversation", target_collection="Conversation"),
        wc.ReferenceProperty(name="field", target_collection="FormField")
    ],
    vector_config=wc.Configure.Vectors.text2vec_openai(),
    generative_config=wc.Configure.Generative.openai(),
)

Answer = client.collections.create(
    name="Answer",
    properties=[
        wc.Property(name="field_key", data_type=wc.DataType.TEXT),
        wc.Property(name="value_text", data_type=wc.DataType.TEXT),
        wc.Property(name="summary", data_type=wc.DataType.TEXT)
    ],
    references=[
        wc.ReferenceProperty(name="conversation", target_collection="Conversation"),
        wc.ReferenceProperty(name="field", target_collection="FormField"),
        wc.ReferenceProperty(name="from_utterances", target_collection="Utterance")
    ],
    vector_config=wc.Configure.Vectors.text2vec_openai()
)

print("✅ Schema created.")
client.close()
