# Text Processing API Key Assignment

This repository contains a Flask API with `X-API-Key` authentication and cURL testing commands as per Task 2 requirements.

## API Key Assignment & Testers
1. **Consumer 1:** `key_consumer_1`
2. **Consumer 2:** `key_consumer_2`
3. **Consumer 3:** `key_consumer_3`

---

## How to Run the Server

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python app.py
   ```

---

## Testing with cURL Commands

### 1. Test Valid Key (Consumer 1)
```bash
curl -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: key_consumer_1"   -d '{"text": "hello rootsoftware"}'
```
**Expected Response:** `200 OK` with uppercase text `"HELLO ROOTSOFTWARE"`.

### 2. Test Valid Key (Consumer 2)
```bash
curl -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: key_consumer_2"   -d '{"text": "flask api key authentication"}'
```

### 3. Test Valid Key (Consumer 3)
```bash
curl -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: key_consumer_3"   -d '{"text": "testing third key"}'
```

### 4. Test Invalid Key (Rejection Test)
```bash
curl -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: invalid_secret_key"   -d '{"text": "test data"}'
```
**Expected Response:** `403 Forbidden` (`Invalid API Key!`).

### 5. Test Missing Key (Rejection Test)
```bash
curl -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -d '{"text": "test data"}'
```
**Expected Response:** `401 Unauthorized` (`API Key Missing!`).
