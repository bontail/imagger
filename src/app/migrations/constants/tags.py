def create_tags(apps, schema_editor) -> None:
    Tag = apps.get_model("app", "Tag")

    data = [
        'Nature',
        'Space',
        'Education',
        'Environment',
        'Programming',
        'Technology',
        'Buildings',
        'Flowers',
        'Animals',
        'Cats',
        'Dogs',
        'Python'
    ]

    tags = [Tag(name=name) for name in data]
    Tag.objects.bulk_create(tags)
