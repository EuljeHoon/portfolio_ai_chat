from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import ask_ai

@api_view(["POST"])
def chat(request):
    message = request.data.get("message", "")

    if not message:
        return Response({"error": "Message is required"}, status=400)

    answer = ask_ai(message)
    return Response({"answer": answer})