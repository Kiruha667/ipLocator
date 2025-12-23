from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/city")
def get_city_from_ip(ip: str):
    try:
        external_url = f"http://ip-api.com/json/{ip}"
        response = requests.get(external_url)

        data = response.json()
        city_name = data.get("city", "Не удалось определить город")

        return {
            "requested_ip": ip,
            "city": city_name,
            "status": "success"
        }

    except Exception as e:
        return {"error": str(e)}