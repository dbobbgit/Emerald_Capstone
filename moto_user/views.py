from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import MotoUser
from .forms import EditProfileForm
# Create your views here.

def MotoUserView(request, user_id: int):
    profile= MotoUser.objects.get(id=user_id)
    return render(request, 'profile.html', {"profile":profile})




def EditProfileView(request, user_id: int):
    ''' CAITLIN: ALLOWS USER TO EDIT THEIR PROFILE WITH FIELDS 
    PREVIOUSLY ENTERED INFO. ONCE USER SAVES INFO, AS OF 7/10 COMMIT 
    THEY ARE REROUTED TO HOMEPAGE ON WHICH AN HREF HAS BEEN ADDED AROUND
    THE USER'S USERNAME TO PROVIDE A LINK TO THEIR PROFILE'''
    current_profile= MotoUser.objects.get(id=user_id)
    if request.user.is_staff or request.user == MotoUser.username.user:
        if request.method == "POST":
            form = EditProfileForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                current_profile.display_name = data['display_name']
                current_profile.bio = data['bio']
                current_profile.bike = data['bike']
                current_profile.riding_style = data['riding_style']
                current_profile.riding_level = data['riding_level']
                current_profile.save()
                return HttpResponseRedirect(reverse("home"))
        
        form = EditProfileForm(initial={
            'display_name': current_profile.display_name,
            'bio': current_profile.bio,
            'bike': current_profile.bike,
            'riding_style': current_profile.riding_style,
            'riding_level': current_profile.riding_level
        })

        return render(request, "edit_profile.html", { "form": form})

    return HttpResponseRedirect(reverse("home"))