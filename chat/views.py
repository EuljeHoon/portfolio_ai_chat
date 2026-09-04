from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import ask_ai


def health(request):
    """Lightweight health/warm-up endpoint.

    Returns an immediate 200 with no DB access, no AI calls, and no auth or
    throttling. Its only purpose is to wake the server process on Render's
    free tier before the user sends a real question.
    """
    return JsonResponse({"status": "ok"})

@api_view(["POST"])
def chat(request):
    message = request.data.get("message", "")

    if not message:
        return Response({"error": "Message is required"}, status=400)

    answer = ask_ai(message)
    return Response({"answer": answer})