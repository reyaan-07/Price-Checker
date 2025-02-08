from app import app  # Change 'app' to your actual module name

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug= True)