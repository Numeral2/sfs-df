import bcrypt

# Lozinka koju želiš hasirati
password = "tvoja_lozinka"  # Zamijeni s pravom lozinkom

# Generiraj hash lozinke
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Ispiši hash koji ćeš pohraniti u .env
print(hashed_password)

