from django.shortcuts import render
from accounts.models import UserData
from django.shortcuts import redirect

def index(request):
    if request.user.is_authenticated:
        user_data = UserData.objects.filter(user=request.user).first()
    else:
        return render(request, 'index.html')

    return render(request, 'index.html', {'user_data': user_data})

def test(request):
    return render(request, 'componenten/test.html')