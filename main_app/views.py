# main_app/views.py

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


from .models import Watch, Bid, Transaction, Tag
from .forms import WatchForm, BidForm

# Define the home view function
def home(request):
    watches = Watch.objects.filter(is_available=True, is_sold=False)
    return render(request, 'home.html', {'watches': watches})

#Signup View
def signup(request):
    error = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Signup failed. Try again.'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'error': error})

#Dashboard View
@login_required
def dashboard(request):
    user_watches = Watch.objects.filter(owner=request.user)
    user_bids = Bid.objects.filter(bidder=request.user)
    transactions = Transaction.objects.filter(buyer=request.user) | Transaction.objects.filter(seller=request.user)
    return render(request, 'dashboard.html', {
        'user_watches': user_watches,
        'user_bids': user_bids,
        'transactions': transactions,
    })

#Public View
def profile(request, user_id):
    user_profile = User.objects.get(id=user_id)
    user_watches = Watch.objects.filter(owner=user_profile)
    return render(request, 'profile.html', {'user_profile': user_profile, 'user_watches': user_watches})

#Detail and Bidding View
@login_required
def watch_detail(request, pk):
    watch = Watch.objects.get(id=pk)
    bid_form = BidForm()
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            new_bid.watch = watch
            new_bid.bidder = request.user
            new_bid.save()
            return redirect('watch_detail', pk=pk)
    bids = watch.bids.all().order_by('-amount')
    return render(request, 'watch_detail.html', {
        'watch': watch,
        'bids': bids,
        'bid_form': bid_form
    })

#Create watch
class WatchCreate(LoginRequiredMixin, CreateView):
    model = Watch
    form_class = WatchForm
    template_name = 'watch_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

#Update watch
class WatchUpdate(LoginRequiredMixin, UpdateView):
    model = Watch
    form_class = WatchForm
    template_name = 'watch_form.html'

#Delete watch 
class WatchDelete(LoginRequiredMixin, DeleteView):
    model = Watch
    success_url = '/'
    template_name = 'watch_confirm_delete.html'