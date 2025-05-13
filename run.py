from app import app

if __name__ == "__main__":
    print("Investment App is running...")
    app.run(host='0.0.0.0', port=9020, debug=True)
