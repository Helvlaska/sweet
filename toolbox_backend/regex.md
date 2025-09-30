# Regex

### 🔹 1. Email

```python
^[\w\.-]+@[\w\.-]+\.\w+$
```

➡️ Vérifie le format classique d’un email (test@mail.com).

---

### 🔹 2. Mot de passe (robuste)

```python
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

➡️ Au moins :

- 1 minuscule,
- 1 majuscule,
- 1 chiffre,
- 1 caractère spécial,
- longueur ≥ 8.

---

### 🔹 3. Texte safe (anti-injection)

```python
^[a-zA-Z0-9\s.,!?'"()-]+$
```

➡️ Autorise lettres, chiffres, espaces, ponctuation simple.
⚠️ Bloque < script> et autres caractères suspects.

---

### 🔹 4. Numérique entier

```python
^\d+$
```

➡️ Vérifie que la valeur est un entier positif.

---

### 🔹 5. Décimal (float)

```python
^\d+(\.\d+)?$
```

➡️ Vérifie que la valeur est un nombre décimal positif.
