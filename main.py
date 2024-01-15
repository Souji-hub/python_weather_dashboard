from weather_functions import create_weather_dashboard

if __name__ == "__main__":
    # Call the main function to run the program
    with open('api_key.txt', 'r') as file:
        api_key = file.read().strip()

    create_weather_dashboard(api_key)
