import requests
data = {"email":"twd@gmail.com","password":"dunamis2006"}
req = requests.post(f"http://localhost:8000/api/v1/auth/login",
	headers = {"Content-Type":"application/json"},json = data)
# req = requests.delete(f"http://localhost:8000/api/v1/cart/add/{product_id}",
	# headers = {"Authorization":"Token "+token},data = {"quantity":10})

print(req.json())