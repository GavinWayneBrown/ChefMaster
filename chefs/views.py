from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, EditBioForm, CustomUserChangeForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm 
    success_url = reverse_lazy("login") 
    template_name = "registration/signup.html"

@login_required
def edit_bio(request):
    user = request.user
    if request.method == 'POST':
        form = EditBioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('recipes_by_author', author_id=user.pk)
    else:
        form = EditBioForm(instance=user)
    return render(request, 'recipe/edit_bio.html', {'form': form})

