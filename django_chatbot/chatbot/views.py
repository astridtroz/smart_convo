
from django.shortcuts import render,reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai

genai.configure(api_key="AIzaSyCYApkE10QFVNNIR4NL7Ew4cTSPk10fzwM")

@login_required
def ask_questions(request):
    if request.method=='POST':
        text=request.POST.get("text")
        model=genai.GenerativeModel("gemini-pro")
        chat=model.start_chat()
        response=chat.send_message(text)
        user=request.user
        ChatBot.objects.create(text_input=text,gemini_output=response.text, user=user)
        
        response_data={
            "text": response.text,
        }
        return JsonResponse({"data": response_data})
    else:
        return HttpResponseRedirect(
            reverse("chat")
        )

@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chatbot.html", {"chats": chats})