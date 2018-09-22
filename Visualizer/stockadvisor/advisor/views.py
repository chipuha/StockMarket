from django.shortcuts import render

def index(request):
    context = {'ticker': 'TSLA'}
    return render(request,'advisor/index.html',context)
