from typing import Any

DB_PATH = "../main_sqlite.db"
TEST_DB_PATH = "../test_sqlite.db"
ERROR_RESPONSES: dict[int, Any] = {
    401: {
        "content": {
            "application/json": {
                "example": {"error": {"message": "Invalid admin API key <key>"}}
            }
        }
    },
    404: {
        "content": {
            "application/json": {
                "example": {"error": {"message": "User does not exist."}}
            }
        }
    },
    409: {
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "User with username <username> already exists."
                    }
                }
            }
        }
    },
}
