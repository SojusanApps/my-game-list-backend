from _typeshed import Incomplete
from typing import ClassVar
from django.db import migrations

def populate_jti_hex(apps: Incomplete, schema_editor: Incomplete) -> None: ...
def reverse_populate_jti_hex(apps: Incomplete, schema_editor: Incomplete) -> None: ...

class Migration(migrations.Migration):
    dependencies: ClassVar[Incomplete]
    operations: ClassVar[Incomplete]
