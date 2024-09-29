from django.shortcuts import render,HttpResponse,redirect
from .models import food
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from django.urls import reverse
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def new(request):
    if request.user.is_anonymous:
        return redirect('signup')
    return render(request,"index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect('signup')
        
        else:
             user=User.objects.create_user(username=username,password=password)
             login(request,user)
             return redirect('home')

    return render(request,'signup.html')

def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return redirect('signup')


    return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect('signin')

def submit(request):
    if request.method == 'POST':
        item1 = request.POST.get('item1')
        item2 = request.POST.get('item2')
        item3 = request.POST.get('item3')
        item4 = request.POST.get('item4')
        q1 = request.POST.get('q1')
        q2 = request.POST.get('q2')
        q3 = request.POST.get('q3')
        q4 = request.POST.get('q4')

        # Save the food entry
        f1 = food(item1=item1, item2=item2, item3=item3, item4=item4, q1=q1, q2=q2, q3=q3, q4=q4)
        f1.save()

        # Retrieve all food entries for plotting
        # details = food.objects.all()
        details=food.objects.latest('id')

        # Collect all items and quantities
        # for detail in details:
        items=[details.item1, details.item2, details.item3, details.item4]
        quantities=[details.q1, details.q2, details.q3, details.q4]

        # Create the DataFrame
        data = pd.DataFrame({
            'Items': items,
            'Quantities': pd.to_numeric(quantities, errors='coerce')  # Ensure quantities are numeric
        })

        # Create the plot
        # sns.barplot(x='Items', y='Quantities', data=data)
        sns.barplot(x='Quantities', y='Items', data=data)
        for index, row in data.iterrows():
            plt.text(row['Quantities'] + 0.5, index, row['Quantities'], color='black', va='center')
        # plt.bar(items,quantities)
        # plt.xlim(left=0)
        # plt.ylim(bottom=0)
    
        # Save the graph
        static_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'graph.jpg')
        plt.xlabel('Quantities', fontsize=16)  # Change fontsize as needed
        plt.ylabel('Items', fontsize=16)
        plt.savefig(static_path)
        plt.clf()
        static_path = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'pie.jpg')
        plt.pie(data['Quantities'], labels=data['Items'], autopct='%1.1f%%', startangle=140)
        plt.savefig(static_path)
        plt.clf()  # Clear the plot
         

        return render(request, "submit.html")
    

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login


from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

    






    







