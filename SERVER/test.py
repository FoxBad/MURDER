import random

roles = ["assassin", "innocent", "murder"]
role = random.choice(roles)
roles.remove(role)

print(roles, role)