#!/bin/bash

bash -c "cd app && alembic revision --autogenerate && alembic upgrade head"
bash -c "cd app && python initial_data.py"
exec "$@"