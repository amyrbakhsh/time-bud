# main_app/views.py

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Watch, Bid, Transaction, Tag
from .forms import WatchForm, BidForm
from django.http import HttpResponseForbidden

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
    watches = Watch.objects.filter(owner=request.user)
    user_bids = Bid.objects.filter(bidder=request.user)
    bids_on_user_watches = Bid.objects.filter(watch__owner=request.user, watch__is_sold=False).order_by('-created_at')
    transactions = Transaction.objects.filter(buyer=request.user) | Transaction.objects.filter(seller=request.user)
    sold_watch_ids = Transaction.objects.filter(seller=request.user).values_list('watch_id', flat=True)
    return render(request, 'dashboard.html', {
        'watches': watches,
        'bids': user_bids,
        'bids_on_user_watches': bids_on_user_watches,
        'transactions': transactions,
        'sold_watch_ids': sold_watch_ids,
    })


#Watch Detail
def watch_detail(request, pk):
    watch = Watch.objects.get(id=pk) 
    ... 
    return render(request, 'watch/watch_details.html', {
        'watch': watch,
        'bid_form': bid_form
    })

#Public View
def profile(request, user_id):
    user_profile = User.objects.get(id=user_id)
    user_watches = Watch.objects.filter(owner=user_profile)
    return render(request, 'profile.html', {'user_profile': user_profile, 'user_watches': user_watches})

#Profile View
def profile_view(request, username):
    profile_user = User.objects.get(username=username)
    watches = Watch.objects.filter(owner=profile_user)
    bids = Bid.objects.filter(bidder=profile_user)
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'watches': watches,
        'bids': bids
    })



def tag_list(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    watches = tag.watches.filter(is_available=True, is_sold=False)
    return render(request, 'tag_list.html', {
        'tag': tag,
        'watches': watches
    })


#Detail and Bidding View
@login_required
def watch_detail(request, pk):
    watch = Watch.objects.get(id=pk)
    bid_form = BidForm()
    if watch.is_sold:
        bids = watch.bids.all().order_by('-amount')
        return render (request, 'watch/watch_details.html', {
            'watch': watch,
            'bids': bids,
            'bid_form': None,
            'is_sold': True,
        })
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            new_bid.watch = watch
            new_bid.bidder = request.user
            new_bid.save()
            return redirect('watch_detail', pk=pk)
    bids = watch.bids.all().order_by('-amount')
    return render(request, 'watch/watch_details.html', {
        'watch': watch,
        'bids': bids,
        'bid_form': bid_form,
        'is_available': True,
    })
#transaction views
@login_required
def my_transactions(request):
    sold = Transaction.objects.filter(seller=request.user)
    bought = Transaction.objects.filter(buyer=request.user)
    return render(request, 'transactions.html', {
        'sold': sold,
        'bought': bought
    })

#Create watch
class WatchCreate(LoginRequiredMixin, CreateView):
    model = Watch
    form_class = WatchForm
    template_name = 'watch/watch_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

#Add watch
def add_watch(request):
    if request.method == 'POST':
        form = WatchForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('watch_list')  
    else:
        form = WatchForm()
    return render(request, 'add_watch.html', {'form': form})

#Update watch
class WatchUpdate(LoginRequiredMixin, UpdateView):
    model = Watch
    form_class = WatchForm
    template_name = 'watch/watch_form.html'

#Delete watch 
class WatchDelete(LoginRequiredMixin, DeleteView):
    model = Watch
    success_url = '/dashboard'
    template_name = 'watch/watch_confirm_delete.html'

    # Accept Bid View
@login_required
def accept_bid(request, bid_id):
    bid = Bid.objects.get(id=bid_id)
    watch = bid.watch

    if request.user != watch.owner:
        return HttpResponseForbidden("You are not allowed to accept this bid.")

    # Create a transaction record
    Transaction.objects.create(
        watch=watch,
        buyer=bid.bidder,  
        seller=watch.owner,
        final_price=bid.amount
    )

    # Optional: mark as sold
    # watch.owner = bid.bidder
    watch.is_sold = True
    watch.is_available = False
    # watch.auction_end_time = None
    watch.save()
    messages.success(request, f"Bid of ${bid.amount} accepted. Watch sold to {bid.bidder.username}.")

    return redirect('dashboard')

    # return redirect('watch_detail', pk=watch.id)

# Start Auction View
@login_required
def start_auction(request, watch_id):
    watch = Watch.objects.get(id=watch_id)

    if request.user != watch.owner:
        return HttpResponseForbidden("You are not allowed to auction this watch.")

    watch.is_available = True
    watch.save()

    return redirect('dashboard')
