from django.shortcuts import render
from django.views import View
from embed_video.backends import detect_backend
# Create your views here.


class HomeView(View):
    def get(self,request,*args,**kwargs):
        video_url = "https://www.youtube.com/watch?v=n2a2ptmDBXY"
        backend = detect_backend(video_url)
        context = {
            'video_url': video_url,
            'backend': backend,
        }
        return render(request,"home.html",context)
    

    

        
        



