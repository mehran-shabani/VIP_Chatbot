from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import APIRequest, APIResponse
from .prompts_engineering import generate_prompt
from .response_generator import get_model_response
from .cleaner_response_engine import clean_response
from .cot import apply_cot
from .self_consistency import apply_self_consistency
from .ram import cache_instance  # استفاده از نمونه کش پیشرفته

@csrf_exempt
@api_view(['POST'])
def custom_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"detail": "نام کاربری یا رمز عبور ارسال نشده است."},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        return Response({
            "detail": "لاگین موفقیت‌آمیز بود.",
            "sessionid": session_key
        }, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "نام کاربری یا رمز عبور اشتباه است."},
                        status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
def custom_logout_view(request):
    logout(request)
    return Response({"detail": "خروج با موفقیت انجام شد."},
                    status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def chat_request(request):
    if not request.user.is_authenticated:
        return Response({"detail": "لطفاً ابتدا لاگین کنید."},
                        status=status.HTTP_401_UNAUTHORIZED)

    user_input = request.data.get("user_input", "").strip()
    if not user_input:
        return Response({"detail": "ورودی نامعتبر است."},
                        status=status.HTTP_400_BAD_REQUEST)

    # بررسی کش برای جلوگیری از پردازش مجدد
    cached_response = cache_instance.get_cached_response(user_input)
    if cached_response:
        return Response({"response": cached_response})

    # ثبت درخواست در دیتابیس
    api_req = APIRequest.objects.create(
        user_input=user_input,
        model_used="Multi-Model"
    )

    prompt = generate_prompt(user_input)
    model_names = ["claude-3-5-sonnet-20240620", "gpt-4o-mini-2024-07-18", "deepseek-coder",]
    raw_responses = []

    for m in model_names:
        raw_resp = get_model_response(prompt, model=m)
        APIResponse.objects.create(
            api_request=api_req,
            model_name=m,
            raw_response=raw_resp
        )
        raw_responses.append(raw_resp)

    # اعمال Chain-of-Thought روی هر پاسخ
    for partial_resp in api_req.responses.all():
        cot_version = apply_cot(partial_resp.raw_response)
        partial_resp.cot_response = cot_version
        partial_resp.save()

    # انتخاب بهترین پاسخ با Self-Consistency
    best_raw_response = apply_self_consistency(raw_responses, user_input)
    final_response = clean_response(best_raw_response)

    # ذخیره پاسخ در کش و آپدیت در دیتابیس
    cache_instance.cache_response(user_input, final_response)
    api_req.final_response = final_response
    api_req.save()

    return Response({"response": final_response})
