
from contextlib import nullcontext
from os import remove
from unicodedata import category
from django.db.models.functions import Lower
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

from .models.product import Product
from .models.customer import Customer
from .models.ui import UI
from .models.disease import Disease
from .models.orders import Order

import joblib as jb
model= jb.load('trained_model')
diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


hash_table = {
    'Fungal infection':['Turmeric','Aloevera','CoconutOil','TeaTree','Cat Claw','CastorOil'],
    'Allergy':['Astragalus','EucalyptusOil','LemonOil','Honey'],
    'GERD':['Ginger','MilkThristle','Caraway','Turmeric','Lemon Balm','Chamomile','GardenAngelica','GreaterCelandine'],
    'Chronic cholestasis':['Milk Thristle','Guar Gum','Activated Charcoal','Dandelian Root'],
    'Drug Reaction':['Activated Charcoal','Aloevera','Coconut Oil','Soda','Tea Tree','Indigo Naturalis'],
    'Peptic ulcer diseae':['Soyabean','Apple','Broccoli','Green Tea','Kale','Cat Claw'],
    'AIDS':['Aloevera'],
    'Diabetes':['Ginger','Aloevera','Ginseng','Cinnamon','Chromium','Gymnema'],
    'Gastroenteritis':['Peppermint','Ginger','Turmeric','Greater Celandine','Activated Charcoal','Apple','Cinnamon','Banana','Kiwi'],
    'Bronchial Asthma':['Honey','Turmeric','Ginseng','Black Seed','Garlic','Cocoa'],
    'Hypertension':['Ginseng'],
    'Migraine':['Peppermint','Ginger','CofeeBeans','Butterbur','Coriander','Valerian'],
    'Cervical spondylosis':['Ginger','Turmeric','Ginseng','Castor Oil','Ghee'],
    'Paralysis (brain hemorrhage)':['Broccoli','Apple','Ginseng','Grapes','Carrot','Tomato','Orange','Melon','Soyabean'],
    'Jaundice':['Ginger','Grapes','Tomato','Lemon','Amla','Tulsi Leave'],
    'Malaria':['Honey','Ginger','Turmeric','Aloevera','Green Tea','Cinnamon','Grapes','Tulsi Leave','Magnifera Indica'],
    'Chicken pox':['Honey','Aloevera','Tulsi Leaves','Chamomile'],
    'Dengue':['Turmeric','Orange','Tulsi Leave','Neem Leave','Papaya Leave','Giloy','Black Pepper'],
    'Typhoid':['Apple','Garlic','Orange','Banana'],
    'Hepatitis A':['Peppermint','Ginger','Milk Thristle','Green Tea','Tomato'],
    'Hepatitis B':['Milk Thristle','Valerian','Tomato','Misletoe','Artemesia','Green Tea'],
    'Hepatitis C':['Milk Thristle','Green Tea','Tomato'],
    'Hepatitis D':['Milk Thristle','Green Tea','Tomato'],
    'Hepatitis E':['Milk Thristle','Green Tea','Tomato'],
    'Alcoholic Hepatitis':['Turmeric','Dandelion','Apple','Coffee Bean','Carrot','Amla','Papaya Leave','Avocado'],
    'Tuberculosis':['Peppermint','Ginger','Green Tea','Garlic','Soyabean','Amla','Banana','Peanuts'],
    'Common Cold':['Honey','Ginger','Garlic'],
    'Pneumonia':['Peppermint','Eucalyptus Oil','Honey','Ginger','Turmeric','Tea Tree','Coffee Beans'],
    'Dimorphic Hemmorhoids(piles)':['Greater Celandine','Guar Gum','Coconut Oil','Aloevera','Tea Tree','Apple','Cat Claw','Kiwi'],
    'Heart Attack':['Ginger','Guar Gum','Apple','Cocoa','Tulsi Leave','Fenugreek','Almond','Kiwi'],
    'Varicose Veins':['Lemon Oil','Apple','Garlic','Orange','Olive Oil'],
    'Hyperthyroidism':['Lemon Balm','Cocoa','Capsaicin','Bugleweed'],
    'Hypoglycemia':['Honey','Dandelion','Melon','Olive Oil'],
    'Osteoarth':['Eucalyptus Oil','Ginger','Turmeric','Coconut Oil','Aloevera','Green Tea','Cat Claw','Thunder God Vine'],
    'Arthritis':['Cat Claw','Thunder God Vine'],
    '(vertigo)Paroymsal Positional Vertigo':['Honey','Ginger','Apple','Almond'],
    'Acne':['Tea Tree','Apple','Castor OIl','Chamomile','Neem Leave','Lavender Oil'],
    'Urinary Tract Infection':['Grape','Orange','Capsaicin','Kiwi'],
    'Psoriasis':['Turmeric','Aloevera','Tea Tree','Apple','Castor Oil','Capsicin','Thunder God Vine'],
    'Impetigo':['Ginger','Garlic','Aloevera','Tea Tree','Chamomile','Banana','Fenugreek','Grapes'],
    'Hypothyroidism':['Ginger','Broccoli','Apple','Ginseng','Tulsi Leave'],

}

symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
    'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
    'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
    'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
    'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
    'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
    'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
    'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
    'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
    'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
    'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
    'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
    'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
    'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
    'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
    'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
    'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
    'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
    'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
    'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
    'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
    'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
    'yellow_crust_ooze']

alphabaticsymptomslist = sorted(symptomslist)

        
    
       

res = None
pro_list=[]
def home(request):
    if request.method=='GET':
        return render(request, 'home.html',{'list1':alphabaticsymptomslist})

    else:
        pro_list.clear()
        s1=None
        s2=None
        s3=None
        s4=None
        s5=None
        s1 = request.POST.get('sym1')
        s2 = request.POST.get('sym2')
        s3 = request.POST.get('sym3')
        s4 = request.POST.get('sym4')
        s5 = request.POST.get('sym5')
        if(s1 or s2 or s3 or s4 or s5):
            ######################################################################################
            inputes=[s1,s2,s3,s4,s5]
            print(inputes)
            input_arr =[]
            for i in range(len(symptomslist)):
                input_arr.append(0)

            for i in range(len(symptomslist)):
                for j in inputes:
                    if symptomslist[i]==j:
                        input_arr[i]=1    
            inputtest=[input_arr]
            ###########################################################################################
            predicted = model.predict(inputtest)
            ###########################################################################################
            res = predicted[0]
            n= len(res)
            lst = [char for char in res]
            if lst[n-1]==' ':
                lst.pop()
            res = ''.join(lst)

        else:
            res = None
        if res:
            dis= Disease.get_disease_name(res)
            if dis:
                herblist = hash_table.get(dis.name)
            else:
                herblist = None
        if herblist is not None:
            for i in herblist:
                product = Product.get_products_by_name(i)
                if product is not None:
                    pro_list.append(product)
        print(pro_list)
        return render(request, 'home.html',{'list1':alphabaticsymptomslist, 'disease': res, 'herbs':herblist, 'pro_list':pro_list})

################################### Index Page #################################################################
def index(request):
    banner = UI.get_element_by_name("banner")
    prediction =UI.get_element_by_name("prediction")
    shop =UI.get_element_by_name("shop")
    business =UI.get_element_by_name("business")
    logov = UI.get_element_by_name("logov")
    ui = {
        "logov":logov,
        "banner": banner,
        "prediction":prediction,
        "shop":shop,
        "business":business
    }
    return render(request,"index.html",ui)

########################## Store Page ########################################################
def store(request):
    products = None
    category_name= request.GET.get('query')
    if category_name:
        products = Product.get_all_products_by_name(category_name)
    else:
        products = Product.get_all_products()
    data ={}
    data['products']=products
    cart = request.session.get('cart')
    if not cart:
        request.session['cart']={}
    
    if request.method=='POST':
        product= request.POST.get('product')
        cart = request.session.get('cart')
        remove =request.POST.get('remove')
        print("this is product",product)
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity==1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1    
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart']) 
    return render(request, 'store.html', data)

########################### Herb Recommendation  #############################################################################
def recommend(request):
    prod_list=set(pro_list)
    if request.method=='POST':
        product= request.POST.get('product')
        cart = request.session.get('cart')
        remove =request.POST.get('remove')
        print("this is product",product)
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity==1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1    
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart']) 
        print(pro_list)
        print(res)

    return render(request, 'home.html', {'list1':alphabaticsymptomslist, 'pro_list':prod_list, 'disease':res})


########################### Cart ##############################################################################
def cart(request):
    if request.session.get('cart') is not None:
        bag = list(request.session.get('cart').keys())
        product = Product.get_products_by_id(bag)

    else:
        product = None
    return render(request, 'cart.html',{'products': product})
    
######################## Sign In Page ##########################################################################
def signin(request):
    error_message = None
    if request.method == "GET":
        return render(request, 'signin.html')
    else:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        value={
            'firstname':firstname,
            'lastname':lastname,
            'email': email
            }

        if(len(password1)>=6 and len(password2)>=6):
            if(password1==password2):
                password = password1 
                customer = Customer(firstname = firstname,lastname=lastname,email=email,password=password)
                if customer.isExist():
                    error_message = 'Email Address Already Registered..'
                else:
                    customer.password = make_password(customer.password)
                    customer.register()
                    return render(request,'home.html')
            else:
                error_message = "Passwords did not Matched!"
                
        else:
            error_message = "Password must be 6 or more characters long!"
        data={
            'error': error_message,
            'values': value
            }

        return render(request,'signin.html',data)

######################## Log In Page ##########################################################################
def login(request):
    if request.method=='GET':
        
        return render(request, 'login.html')

    else:
        request.session['cart'] = {}
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message= None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer']=customer.id
                request.session['customer_email']=customer.email
                return redirect('homepage')
            else:
                error_message='Email Or Password Is Invalid..!'    
        else:
            error_message='Email Or Password Is Invalid..!'  
        return render(request,'login.html',{'error':error_message})

######################## LOG OUT ##########################################################################
def logout(request):
    request.session.clear()
    return render(request, 'login.html')

######################## CHECKOUT ##################################################################################
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(customer = Customer(id = customer),
                          product = product,
                          price = product.price,
                          address = address,
                          phone = phone,
                          quantity = cart.get(str(product.id)))
            order.placeOrder()

        request.session['cart'] = {}

        return render(request, 'cart.html')

######################## ORDERS ##########################################################################
def orders(request):
    customer = request.session.get('customer')
    order = Order.get_orders_by_customer_id(customer)
    print(order)
    return render(request, 'orders.html',{'orders':order})
