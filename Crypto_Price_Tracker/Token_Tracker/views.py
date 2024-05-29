from django.shortcuts import render, HttpResponse
import requests
from .forms import SearchForm
from django.http import JsonResponse
import os
# Create your views here.

API_END_POINT = "https://api.coingecko.com/api/v3"
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-FMrnmbuUU7FZ2K73t2jYdaVk"
}

def get_data():
    parameters = {
        "ids": "bitcoin,ethereum,solana",
        "vs_currencies": "ZAR",
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }

    response = requests.get(f"{API_END_POINT}/simple/price", params=parameters, headers=headers)
    return response.json()

def custom_search(user_query):
    parameters = {
        "ids": user_query.lower(),
        "vs_currencies": "ZAR",
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }

    response = requests.get(f"{API_END_POINT}/simple/price", params=parameters, headers=headers)
    return response.json()


def index(request):
    response = get_data()
    parameters = {
        "btc_price": response["bitcoin"]['zar'],
        "btc_cap": round(response["bitcoin"]['zar_market_cap'],2),
        "btc_24h": round(response["bitcoin"]['zar_24h_change'],2),
        "eth_price": response["ethereum"]['zar'],
        "eth_cap": round(response["ethereum"]['zar_market_cap'],2),
        "eth_24h": round(response["ethereum"]['zar_24h_change'],2),
        "sol_price": response["solana"]['zar'],
        "sol_cap": round(response["solana"]['zar_market_cap'],2),
        "sol_24h": round(response["solana"]['zar_24h_change'],2),
    }

    form = SearchForm()
    if request.method == "POST":
        user_query = request.POST.get('search')
        user_search = custom_search(user_query)
        search_params = {
            "search_price": user_search[user_query.lower()]['zar'],
            "search_cap": round(user_search[user_query.lower()]['zar_market_cap'],2),
            "search_24h": round(user_search[user_query.lower()]['zar_24h_change'],2),
        }
        return render(request, "Token_Tracker/index.html", {
        "parameters": parameters,
        "form": form,
        "is_searched": True,
        "searched": search_params,
        "query": user_query,
    })

    return render(request, "Token_Tracker/index.html", {
        "parameters": parameters,
        "form": form,
        "is_searched": False
    })


def info(request, slug):
    user_search = custom_search(slug)
    search_params = {
        "searched_coin": slug.capitalize(),
        "search_price": user_search[slug.lower()]['zar'],
        "search_cap": round(user_search[slug.lower()]['zar_market_cap'],2),
        "search_24h": round(user_search[slug.lower()]['zar_24h_change'],2),
    }
    return JsonResponse(search_params)
