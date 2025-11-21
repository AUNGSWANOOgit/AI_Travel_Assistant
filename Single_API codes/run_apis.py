import subprocess

def main():
    print("\n" + "="*50)
    print("        API WORKSHOP - Choose an API to Run")
    print("="*50)
    print("\n1. Gemini API - AI explanation of PID controllers")
    print("2. OpenWeather API - Get weather forecast")
    print("3. REST Countries API - Get country information")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        print("\n--- Running Gemini API ---\n")
        subprocess.run(["python", "API_Workshop(GEMINI).py"])
    elif choice == "2":
        print("\n--- Running OpenWeather API ---\n")
        subprocess.run(["python", "API_Workshop(OpenWeather).py"])
    elif choice == "3":
        print("\n--- Running REST Countries API ---\n")
        subprocess.run(["python", "API_Workshop(REST_Countries).py"])
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again and choose 1-4.")

if __name__ == "__main__":
    main()
