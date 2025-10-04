from django.shortcuts import render
from rest_framework import generics
from .serilizers import UserRegistrationSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def Registration(request):
    print("📥 Step 1 - Incoming Data from client:",request.data)

    serilizer=UserRegistrationSerializer(data=request.data)
    print("🛠️ Step 2 - Serializer created with data")


    if serilizer.is_valid():
        print("✅ Step 3 - Data is valid")

        user=serilizer.save()
        print("💾 Step 4 - User saved into DB:", user)

        return Response({
            "message": "User registered successfully!",
            "saved_user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    
    else:
        print("❌ Step 3 - Validation failed:", serilizer.errors)
        return Response(serilizer.error,status=400)

@api_view(['post'])
@permission_classes([AllowAny])
def login_user(request):
    print("📥 Step 1 - Incoming Data from client:",request.data)
    
    username=request.data.get("Username")
    password=request.data.get("Password")

    user=authenticate(username=username,password=password)


    if user is not None:
        refresh=RefreshToken.for_user(user)
        print("login successful",user.username)

        return Response({
                "message":"login succesful",
                "username":user.username,
                "email":user.email,
                "roles": list(user.groups.values_list("name", flat=True)),
                "access":str(refresh.access_token),
                "refresh":str(refresh)
                        
                        
            },status=status.HTTP_200_OK)
    else :
        print("login unsuccessful",user.username)
        return Response({"error": "Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)
    


    

#     📝 Django QuerySet Cheat Sheet
# 1️⃣ Fetching Data
# Operation	Example	Description
# All objects	User.objects.all()	Returns all rows as a QuerySet
# Single object	User.objects.get(username="kali")	Fetch single row; raises error if not found or multiple
# Filter	User.objects.filter(is_active=True)	WHERE condition
# Exclude	User.objects.exclude(role="Admin")	NOT condition
# First / Last	User.objects.first(), User.objects.last()	Get first/last object
# Exists	User.objects.filter(is_active=True).exists()	Returns True/False
# Count	User.objects.count()	Returns number of rows
# 2️⃣ Slicing / Ordering
# Operation	Example	Description
# Slice	User.objects.all()[:5]	SQL LIMIT
# Order	User.objects.order_by('username')	Ascending
# Reverse Order	User.objects.order_by('-username')	Descending
# 3️⃣ Extracting Fields
# Operation	Example	Description
# values()	User.objects.values('id','username')	Returns dict: [{'id':1,'username':'kali'}, ...]
# values_list()	User.objects.values_list('username', flat=True)	Returns flat list: ['kali', 'vendor']
# 4️⃣ Aggregation / Annotation
# Operation	Example	Description
# Count	User.objects.aggregate(total=Count('id'))	Returns total count: {'total': 10}
# Annotate	User.objects.annotate(num_groups=Count('groups'))	Adds calculated field per object
# 5️⃣ Chaining
# Example	Description
# User.objects.filter(is_active=True).order_by('username')[:5]	Filters, orders, and slices in one chain
# 6️⃣ Set Operations
# Example	Description
# qs1.union(qs2)	Combines two QuerySets (SQL UNION)
# qs1.intersection(qs2)	SQL INTERSECT
# qs1.difference(qs2)	SQL EXCEPT
# 7️⃣ Updating / Deleting
# Example	Description
# User.objects.filter(is_active=False).update(is_active=True)	Bulk update
# User.objects.filter(role='Temp').delete()	Deletes matching rows
# 8️⃣ Many-to-Many Examples (Groups / Roles)
# user = User.objects.get(username="kali")
# # All groups for user
# groups_qs = user.groups.all()  # <QuerySet [<Group: Admin>, <Group: Vendor>]>

# # Only names
# roles = list(user.groups.values_list("name", flat=True))
# # ['Admin','Vendor']

# # Check if user has Admin role
# if "Admin" in roles:
#     print("Redirect to admin dashboard")

# 9️⃣ Lazy Evaluation Reminder

# QuerySets don’t hit DB until needed:

# Action	Forces DB query?
# for obj in qs	✅
# list(qs)	✅
# qs.count()	✅
# qs.exists()	✅
# qs.first()	✅
# Just defining qs = User.objects.all()	❌