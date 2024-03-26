requirements:
	@pip freeze > requirements.txt

secret:
	@python -c 'import secrets; print(secrets.token_hex(32))'


run:
	@python runserver.py

token:
	@python -c 'import secrets; print(secrets.token_hex(64))'