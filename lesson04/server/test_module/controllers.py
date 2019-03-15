def send_presence(request):
   return {
            "response": 200,
            "msg": f"Hi {request.get('user')['account_name']}"
   }
