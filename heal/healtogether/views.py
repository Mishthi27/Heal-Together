from django.shortcuts import render

# Create your views here.
# Create your views here. 

def index(request): 
    return render(request, 'HealTogether/index.html') 

def login(request): 
    return render(request, 'login.html') 
 
def logout(request): 
    return render(request, 'index.html')  

from django.http import JsonResponse
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# PET scan lab data (with precise locations)
data = {
    "Lab": [
        "Healthians", "Easybookmylab", "Nueclear Healthcare", "House of Diagnostics (HOD)", 
        "Medintu", "Ganesh Diagnostic", "Yashoda Hospital", "Max Healthcare", 
        "Wellness Pathcare", "Metro Hospital", "Scan4Health"
    ],
    "Address": [
        "DLF Towers, Moti Nagar, New Delhi", "Lajpat Nagar, New Delhi", "Green Park, Delhi",
        "Pitampura, New Delhi", "Greater Kailash, New Delhi", "Rohini, Delhi",
        "Kaushambi, Ghaziabad", "Saket, New Delhi", "Gurgaon, Haryana", "Noida, Uttar Pradesh",
        "Sector 44, Gurgaon"
    ],
    "Latitude": [28.66, 28.57, 28.55, 28.70, 28.54, 28.72, 28.65, 28.52, 28.47, 28.60, 28.45],
    "Longitude": [77.12, 77.23, 77.20, 77.15, 77.18, 77.08, 77.32, 77.20, 77.10, 77.25, 77.05],
    "Price": [10999, 10499, np.nan, 9999, 12999, 11950, 10999, np.nan, 16999, np.nan, 10000]
}

df = pd.DataFrame(data)

def get_nearest_lab(request):
    """
    Django view to find the nearest and cheapest PET scan lab.
    User sends their location as a GET request (e.g., ?location=Connaught+Place,Delhi)
    """
    user_location = request.GET.get("location", None)

    if not user_location:
        return JsonResponse({"error": "Location parameter is required"}, status=400)

    geolocator = Nominatim(user_agent="healtogether_locator")
    location = geolocator.geocode(user_location)

    if not location:
        return JsonResponse({"error": "Invalid location"}, status=400)

    user_coords = (location.latitude, location.longitude)

    # Compute distances from user to each lab
    df["Distance"] = df.apply(lambda row: geodesic(user_coords, (row["Latitude"], row["Longitude"])).km, axis=1)

    # Drop rows where price is NaN
    valid_labs = df.dropna(subset=["Price"])

    if valid_labs.empty:
        return JsonResponse({"error": "No labs with price available"}, status=400)

    # Find the best lab (nearest + cheapest)
    best_lab = valid_labs.sort_values(by=["Distance", "Price"]).iloc[0]

    response_data = {
        "lab_name": best_lab["Lab"],
        "address": best_lab["Address"],
        "distance_km": round(best_lab["Distance"], 2),
        "price_inr": int(best_lab["Price"])
    }

    return JsonResponse(response_data)
