# Task 1 — Database-Driven Flask API with Streamlit

## Run
Open two terminals in the assignment root and install requirements with `pip install -r requirements.txt`.

Terminal 1:
```bash
python Task1_Student_API/app.py
```

Terminal 2:
```bash
streamlit run Task1_Student_API/streamlit_app.py
```

Open the local Streamlit URL shown in the terminal. SQLite database `students.db` is created automatically by the Flask app. Keep the Flask terminal running while using Streamlit.

## API quick tests
```bash
curl http://127.0.0.1:5001/students
curl -X POST http://127.0.0.1:5001/students -H "Content-Type: application/json" -d '{"name":"Ali Khan","department":"BSCS","email":"ali@example.com"}'
curl http://127.0.0.1:5001/students/1
curl -X PUT http://127.0.0.1:5001/students/1 -H "Content-Type: application/json" -d '{"name":"Ali Khan","department":"Software Engineering","email":"ali@example.com"}'
curl -X DELETE http://127.0.0.1:5001/students/1
```

## Video demonstration
Add your own public video demonstration link here before submission.
