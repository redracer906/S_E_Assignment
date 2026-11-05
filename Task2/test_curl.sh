#!/bin/bash

echo "=== Testing Valid API Keys ==="
echo "1. Testing Consumer 1 Key:"
curl -s -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: key_consumer_1"   -d '{"text": "hello rootsoftware"}'
echo -e "
"

echo "2. Testing Consumer 2 Key:"
curl -s -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: key_consumer_2"   -d '{"text": "flask api validation"}'
echo -e "
"

echo "3. Testing Consumer 3 Key:"
curl -s -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: key_consumer_3"   -d '{"text": "task 2 submission"}'
echo -e "
"

echo "=== Testing Invalid & Missing Keys ==="
echo "4. Testing Invalid Key:"
curl -s -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -H "X-API-Key: wrong_key_123"   -d '{"text": "test"}'
echo -e "
"

echo "5. Testing Missing Key Header:"
curl -s -X POST http://127.0.0.1:5000/process   -H "Content-Type: application/json"   -d '{"text": "test"}'
echo -e "
"
