from api import create_app
from decouple import config
from api.config.config import config_dict

DEV = config("PROD_ENV", default="dev", cast=str)

app = create_app(config=config_dict[DEV])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=config("PORT", default=5000, cast=int),
    )
