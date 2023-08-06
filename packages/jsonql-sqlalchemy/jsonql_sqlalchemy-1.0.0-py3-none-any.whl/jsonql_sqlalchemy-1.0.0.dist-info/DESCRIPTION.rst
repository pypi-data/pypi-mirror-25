JsonQL-SQLAlchemy
=================

Simple JSON-Based CRUD Query Language for SQLAlchemy

### Installation

For installing JsonQL for SQLAlchemy, just run this command in your shell.

```bash
pip install jsonql-sqlalchemy
```

### Quick Start

After installing JsonQL-SQLAlchemy, just write this code. That's all!

```python
"""Print records in MyModel Table.

(MyModel) SQLAlchemy Model
(session) SQLAlchemy session instance
"""

from jsonql_sqlalchemy import *


class MyQuery(QueryObject):
    model_class = MyModel
    session = session
    fields = qlutils.map_model(MyModel)


if __name__ == "__main__":
    print(MyQuery().read({}))

```

### Example

For more example codes, see in `samples` directory.


