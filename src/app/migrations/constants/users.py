def create_admin(apps, schema_editor) -> None:
    User = apps.get_model("auth", "User")
    User.objects.create_superuser(
        username='admin', email='admin@gmail.com', password='admin'
    )
