"""Hello world script."""

# Standalone scripts can import from the project package
from cat_facts_cli.play import add

print("hello, I am a script.")
print(f"I can use project functions: 2 + 3 = {add(2, 3)}")
