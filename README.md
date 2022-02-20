# Django



## Fundamentals

for creating django project:

```python
pipenv install django
```

### 7

tu settings.py ye qesmat dare be esme installed_apps ke unja barnamehaei ke default nasb shode ro neshun mide. mesle admin, auth, ...

age appe jadidi dorost konim bayad be inja ezafe konim.

### 8

django bar asase modele mvt kar mikone. view request ro migire v response barmigardune (mesle actione ke tu django view migan) 

### 9

tu django template hamun view tu asp hast ke filehaye html hastan.



## Building a Data Model

### 4

vase sakhtane app:

``` python
python manage.py startapp app_name
```

### 5

vase ijade ye model avale hame models ro az django.db import mikonim.

``` python
from django.db import models

class Product(models.Model):
    title = models.CharField(max_lenght=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
```

django khodesh id ro dorost mikone. ama age bekhaym khodemun ye field ro primary key konim bayad attr primary_key = True ro be ye field bedim. injur dg django id dorost nemikone

### 6  choice fields

mesle enum tu c# age bekhaym ye chizi dorost konim bayad az Field.choices estefade konim.

``` python
 MEMBERSHIP_CHOICES = [
        ('B', 'Bronze'),
        ('S', 'Silver'),
        ('G', 'Gold'),
    ]
memebership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')
```

B tu db zakhire mishe.



### 7  One-to-one Relationships

``` python
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, 		 primary_key=True)
```

### 8 One-to-many Relationship

``` python
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
```

### 9  many-to-many Relationship

``` python
promotion = models.ManyToManyField(Product)
```

### 10 circular relationships

in jahaei etefaq miofte ke vabastegie moteqabel hast. bad tu product ye foreign key be collection dare inja ham foreignkey be product mizanim. related_name ro + gozashtim yani ba inke circular relationship bashe okeyim.

``` python
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')
```



## Setting up the DataBase

### 3 creating migrations

``` python
python manage.py makemigrations
```

### 4 running Migrations

``` python
python manage.py migrate
```

### 5 customizing database schema

age bekhay ye table ro etelaate bishtari besh bedim mesle index ya esm avaz konim v ina ye class darim be esme Meta ke tu hamin classe model tarifesh mikonim. bad in class ye seri property dare ke mitunim emal konim

```python
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)

    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]
```



### 6 reverting migrations

vase revert kardan bayad be akharin migrationi ke mikhaym bargardim:

``` python
python manage.py migrate store 0004
```

ba in code be migratione 0004e store barmigarde. bad taqirati ke dashtim (masalan tu 0005) ro bayad az tu code pak konim v file migrationeshunam pak konim.





## ORM Section

### 4 Managers and QuerySets

har model tu django ye attribute be esme object dare ke ye manager bar migardune. manager ye interface az database. 

dar vaqe ma vase gereftane data az attribute objecte un model estefade mikonim.

```python
Product.objects.all() # this returns a query_set
```

ba query_set mitunim az methodaei mesle filter v orderBy v ... estefade konim akhar age bekhaym data ro begirim bayad ya be list tabdil konim ya chandtasho begirim ....

``` python
query_set = Product.objects.all()
query_set.filter().order_by()
```

### 5 

```python
.get(pk=1) 
#pk hamun primary key hast (.get(id=1) ham mishe)
#get ye dune data barmigardune

.exists() #boolean barmigardune
```

### 6

age bekhaym bozorgtar kuchiktar ro filter konim tu methode filter nemitunim az > ya < estefade konim be jash:

``` python
Product.objects.filter(unit_price__gt=20) #>20
#__gt greater than
#__gte greater or equal
#__lt and __lte
```

```python
.filter(unit_price__range=(20, 30))
.filter(collection__id = 1) #relationshipesh
.filter(title__contains='coffee') -> # case sensitive
.filter(title__econtains='coffee') -> # case insensitive
```



### 7 Q

baraye filter or:

``` python
from django.db.models import Q

query_set = Product.object.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) #or
query_set = Product.object.filter(Q(inventory__lt=10) & Q(unit_price__lt=20)) #and
query_set = Product.object.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))#no
```



### 8 F object

baraye refrence dadan be ye field az F estefade mikonim.

``` python
from django.db.models import F

query_set = Product.objects.filter(inventory=F('unit_price')) 
#masalan vase moqayese kardane barabar budane 2 field

query_set = Product.objects.filter(inventory=F('customer__id')) #be fielde ye modele dg ham mishe refrence dad
```

### 9 sorting

```python
queryset = Product.objects.order_by('unit_price', '-title').reverse()
#aval bar asase unit_price badesh title. -title bar ax sort mikone.
#.reverse ham harchi hast ro bar ax mikone
```



### 11 

age az ye jadval faqat yek seri az etelaato bekhaym v nakhaym hame chizo bargardunim az values() estefade mikonim. values dictionary bar migardune

```python
dictionary = Product.objects.values('id', 'title')
dictionary = Product.objects.values('id', 'title', 'collection__id')
dictionary = Product.objects.filter(id__in=a_dictionary) #contains
```



### 12 only and defer

only mesle values kar mikone ama be jaye dictionary instance bar migardune.

defer bar axe only kar mikone (hame joz una)

```python
queryset = Product.objects.only('id', 'title')
queryset = Product.objects.defer('id', 'title')
```



### 13 selecting related

vase az qabl khundane jadvale vabaste

age rabete many bud az prefetch_related estefade mikonim

```python
queryset = Product.objects.select_related('collection').all()
queryset = Product.objects.select_related('collection__anotherCollectionRelation').all()
queryset = Product.objects.prefetch_related('promotion').all()
```



age ye model dashte bashim ke foreign key ye modele dg bashe v bekhaym az modele aval be dovom dastresi dashte bashim, django khodesh vasamun ye field ba un esm + set dorost mikone:

```python
Order.objects.prefetch_related('orderitem_set')
```



### 14 aggregate, Min, Max, ... 

vase be dast avordane min, max, ... az aggregate estefade mikonim.

```python
from django.db.models.aggregates import Count, Max, Min, Avg, Sum

result = Product.objects.aggregate(count=Count('id'))
#age ye fieldi bezarim ke momkene khali bashe (mesle description) tedade unaei ke value daran ro bar migardune.
#count= ro age bezarim ba hamin esmi ke moshakhas kardim key ro vase result dorost mikone result = {'count': 1000}

result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))
# result = {'count': 1000, 'min_price': Decimal('1.06')}
```



### 15 annotation

age bekhaym ye fielde jadid be queryset ezafe konim az annotation estefade mikonim.

tu django ye classe Expression darim ke madare tamame expression ha mishe. expression ha mesle Value (string, int, ...), F (classe F ke qablan goftim mishe refrence dad), Func, Aggregate

``` python
from django.db.models import Value, F
queryset = Customer.objects.annotate(is_new=Value(True))
# in ye sotune jadid be esme in_new dorost mikone ke hamash 1e

queryset = Customer.objects.annotate(new_id=F('id') + 1)
#id qable + 1 ro tu new_id zakhire mikone
```



### 16 calling database functions

```python
from django.db.models import Value, F, Func

queryset = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
# in ye fielde fullname dorost mikone
```

code bala ro mishe kholase kard v az classe Concat tu django estefade kard

``` python
from django.db.models import Value
from django.db.models.functions import Concat

queryset = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')
#inja dg niazi be F object nadarim ama value ro vase fasele bayad bedim chon age nadim fek mikone un ' ' ye field tu databasemune.
                                     
```



### 17 grouping data

``` python
queryset = Customer.objects.annotate(orders_count=Count('order'))
#inja hamun order_sete ke qablan goftim ama tu in model order migire na order_set!
```



### 18 Expression Wrappers

age bekhaym tu expression ye amaliati mesle zarb anjam bedim bayad tu classe expressionWrapper anjam beshe.

``` python
from django.db.models import ExpressionWrapper

discount = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
#output_filed noe khoruji ro moshakhas mikone
queryset = Customer.objects.annotate(discount=discount)
```



### 19 quering generic relationships

ContentType ye class vase khode djangoe. vaqti ye model darim ke nemikhaym ye type khas behesh bedim (masalan tu ye barname customer ye barname dg product) az in class estefade mikonim.

vase tarife modelesh bayad ye content_type tarif konim ke foreignKey dare be ContentType, ye object_id ke az noe integere v vase gereftane Id un modele. ye content_object ham darim ke az noe GenericForeignKey hast v vase gereftane tamame etelaate un modele.

vaqti modelemuno migrate mikonim khode django ye table dorost mikone be esme __django_content_type__ ke tu un hame modelaei ke tu applicationa hastano neshun mide. in table ye id dare ke vase gereftane modele khasemun bayad id un model ro az in jadval dar biarim.

```python
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_models(Product)
query_set = TaggedItem.objects \
	.select_related('tag') \
    .filter(
    	content_type=content_type,
        object_id=1
    )
```



### 20 Custom Managers

age bekhaym code bala ro ye jure dg piade sazi konim ke un kararo be surate zir anjam bede bayad az custom manager estefade konim:

```python
TaggedItem.objects.get_tags_for(Product, 1)
```

vase inkar bayad tu classi ke contentType darim ye CustomManager tarif konim:

```python
class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
	    
        return TaggedItem.objects \
		.select_related('tag') \
    	.filter(
    		content_type=content_type,
	        object_id=obj_id
    	)
```

bad bayad ye field be esme objects tu un model dorost konim v barabare in class bokonimesh:

```python
Class TaggedItem(model.Models):
    ...
    objects = TaggedItemManager()
```



### 22 creating objects

```python
collection = collection()
collection.title = 'title'
collection.feature_product = Product(id=1) # or Product(pk=1)
#or
collection.feature_product_id = 1
collection.save()
```

ye rahe dg hast:

```python
collection = Collection.objects.create(name='name', featured_product_id=1)
```



### 23 Update objects

```python
collection = collection(pk=11)
collection.title = 'title2'
collection.feature_product = None
collection.save()
```

in ravesh ye moshkeli ke dare ine ke age faqat bekhaym ye field ro update konim baqie fielda datashun lost mishe v khali update mishan. vase hamin az get estefade mikonim

```python
collection = Collection.objects.get(pk=11)
```

ye rahe dg:

```python
Collection.objects.filter(pk=11).update(featured_product=None)
```



### 24 Delete Object

```python
collection = collection(pk=11)
collection.delete()
#or
Collection.objects.filter(id__gt=5).delete()
```



### 25 Transactions

age 2ta chizo bekhaym ba ham save konim v age yekish fail shod un yeki ham nashe

```python
from django.db import transaction

@transaction.atomic()
def fucntion(request):
    ...
    
#kole function ro wrap mikone
```

age bekhaym faqat ye qesmato wrap konim:

```python
with transaction.atomic():
    ...
```



### 26 Raw Query

```python
queryset = Product.objects.raw('SELECT * FROM store_product')
#in ba querysetaye dg farq dare methodaye filter v ... nadare
```

age bekhaym ye query bezanim ke tu model nabashe:

``` python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('sql')
```





## Admin Interface

### 3 registering mdels

tu appe asli ye file admin.py hast ke vase register kardane modelamun unja mirim:

```python
admin.site.register(models.Collection)
```

vase inke bejaye esme default esmi ke mikhaym ro namayesh bede tu modeli ke register kardim bayad methode ___str___ ro overide konim:

```python
#in collection class
def __str__(self) -> str:
    return self.title

class Meta:
        ordering = ['title'] #for sorting by title
```



### 4 Customizing the list page

vase inke jadval chizaei ke mikhaym ro neshun bede:

```python
#in admin.py class
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    
admin.site.register(models.Product, ProductAdmin)
```

ye rahe sade tar ine ke az decorator estefade konim injur dg niaz nist khate akhare register ro benevisim:

```python
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    list_editable= ['unit_price']
    list_per_page = 10
    
#alan 2ta sotune title v unit_price ro neshun mide
#chizaei ke tu list_editable mizarim ro mitunim az jadval edit konim
```

another example:

```python
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    # inja ham mishe ordering ro anjam dad
```



### 5 Adding computed columns

```python
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10
	
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
# ye sotune jadid be esme inventory_status dorost mikone ke ya low dare ya ok
#    @admin.display(ordering='inventory') vase ordering ro ezafe mikone ba asase inventory
```



### 6 Selecting Related Objects

age bekhaym be ye fielde khase related dastresi dashte bashim:

```python
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection'] #collection ro mikhune

    def collection_title(self, product):
        return product.collection.title

    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok' 
```



### 7 overriding the base queryset

age bekhaym az foreing key tedad ya chizaei mesle ino hesab konim bayad methode __get_queryset__ ro ke tu admin.modeladmine override konim:

```python
@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
	
	@admin.display(ordering='products_count') # vase ordering
    def products_count(self, collection):
        return collection.products_count #products_count ro bayad annotate konim ke tu methode paein anjam mishe

    def get_queryset(self, request):
        return super().get_queryset(request) \
	    .annotate(products_count=Count('product'))
```



### 8 link to other pages

age bekhaym link befrestim be jaye meqdari ke generate mikardim bayad linke html befrestim vases inkar ham az format_html estefade konim

```python
from django.utils.html import format_html

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return format_html('<a href=>{}</a>', collection.products_count)

```

hala vase inke begim be koja bere bayad href ro por konim vase inkar mikham dynamic link ro dorost kone:

```python
from django.urls import reverse

# reverse in format ro migire: reverse('admin:app_model_page') ke mishe:

@admin.register(models.Collection)
class collectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist')
        return format_html('<a href={}>{}</a>', url, collection.products_count)

#changelist esmie ke be surate default rushe

```

hala age bekhaym querystring ezafe konim ke vase natije ro hamun record bargadune:

```python
from django.utils.html import urlencode

url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))
```



### 9 search for list page

```python
@admin.register(models.Collection)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    search_fields = ['first_name', 'last_name']
    #age bekhaym ba ye chizi shoru she:
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
```



### 10 filtering the list page

```python
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_per_page = 10
	list_filter = ['collection', 'last_update'] #ye filtering khub vase in sotuna mizare
```

vase custom filtering bayad aval ye class dorost konim ke az __admin.SimpleListFilter__ ersbari kone v 2ta methodesho piade sazi konim:

```python
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory' #esmi ke balaye search miad
    parameter_name = '' #chizi ke tu querystring mire
    
    #tu lookups chizaei ke tu panele filter neshun mide ro vared mikonim. vorudi 	 tuple migire ke har tuple ye filter dorost mikone. parametere aval mishe 		chizi ke bayad filter kone v dovomi mishe chizi ke be onvane esme filter 		neshun mide
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    #tu in method logicemuno minevisim ke tahesh ye queryset bar migardunim
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

    #akhare hame ham vase estefade azash esme in classo tu list_filter ezafe 		mikonim
```



### 11 Creating Custom Actions

```python
 @admin.action(description="Clear inventory")
 def clear_inventory(self, request, queryset):
     updated_count = queryset.update(inventory=0)
     #in vase payame bade anjame actione
     self.message_user(
         request,
         f'{updated_count} products were successfully updated.'
     )
    
 #vase estefade ham bayad esmesho tu actionse adminmodelesh ezafe konim:
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_per_page = 10
	list_filter = ['collection', 'last_update'] #ye filtering khub vase in sotuna mizare
```



### 12 customizing forms

tu in bakhsh miad darbare customize karnade formaei ke django dorost mikone mige. mesle create v ina. tu adminModeli ye alame property darim ke mitunim be form ezafe ya kam konim

tu google bezanim django modeladmin hame optionaro mitunim bbinim.



### 13 validations

vase ashnaei bishtar search kon : django validators

masalan vase inke ye adad hadeaqal 1 bashe tu modeli ke mikhaym:

```python
from django.core.validators import MinValueValidator

unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
description = models.TextField(null=True, blank=True)
```

age ye field ro bekhaym optional konim tu modelesh mizarim blank=True



### 14 editing children using inlines

age vase 1 model ye foreign key dashte bashim v bekhaym moqe create kardane item un yeki ham create konim bayad az inlines estefade konim: (tu classe admin)

```python
#ye classe jadid dorost mikonim
#in class ham az modeladmin ersbari mikone v tamame chizaei ke unja darim ro inja ham mitunim dashte bashim mesle autocomplete v ....
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
#be jaye TabularInline mitunim StackedInline bezarim ke un moqe jadvalesh har kodum az fieldash tu ye khat mian

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline] #classe bala ro inja pass midim
    list_display = ['placed_at', 'payment_status', 'customer']
    list_per_page = 10
```



### 15 generic relations

age ye classe generic dashte bashim ke azash ersbari mionim vase add kardanesh be jaye tabularinline ya stackedinline bayad az genericesh estefade konim baqiash mesle qable:

```python
from django.contrib.contenttypes.admin import GenericTabularInline

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
```

### 16

vase register kardane classe tag tu ye appe dg ke dg appe store vabaste be appe tag nabashe

















#part 2 


# Building RESTfull APIs



## 2 what are Restful api

restfull ye seri qanuna vase ertebate client v servere ke peyravi azashun komak mikone systemi ke misazim sari v scalable v reliable v fahme asun v taqire asun bashe. in qanuna 3tan:

Resources, Representations, http methods



## 3  Resources

resource mesle ye object tu applicationemune (mesle Product, ...) ke applicationemun az tariqe url mitune beshun dastresi dashte bashe. dar vaqe patterni ke vase url darim joze in qavanine. mesle 

http://test.com/products

http://test.com/products/1



## 4 Resource Representation

inke chizi ke barmigardunim az noe un model nist v yeki az anvae Html ya xml ya jsone.



## 7 Createing Api Views

aval tu view.py ye method tarif mikonim. bad tu urls.py (khodemun bayad dorostesh konim):

```python
from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list)
]
#product_list esme methodemune ke tu view.py tarif kardim.
```

applicatione aslimun ye url.py khodesh dare. tu liste urlpatternsesh bayad tarif konim ke age be ye esm request umad be kodum file url morajee kone:

```python
#inja age be http:..../store request bedim mire tu file urls.py tu proje store (ke hamun code balae). bad age be http:..../store/products request bedim mire tu methode product_list (bar asase code bala)
urlpatterns = [
    path('store/', include('store.urls')),
]
```

django 2ta classe HttpRequest v HttpResponse dare. ama frameworke rest ke nasb kardim 2ta class dare be esme Request v Response ke behtare qablian. vase estefade azash:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def product_list(request):
    return Response('ok')

```

age bekhaym id bedim:

```python
#in urls.py
# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('products/<id>/', views.product_details),
]
#inja joz adad str ham migire pas bayad injuresh konim:
    path('products/<int:id>/', views.product_details),

# in views.py
@api_view()
def product_details(request, id):
    return Response(id)
```



## 8 Serializer

tu rest framework ye JSONRender darim ke dictionary migire v json barmigardune. serializer miad objecto migire v tabdil be dictionary mikone. vase in kar ye file serializers.py dorost mikonim v tu un fieldaei az modelemun ke mikhaym serialize konim ro tarfi mikonim:

(tu django-rest-framework.org bakhshe api guid serialize fields liste kameleshun hast) 

```python
from rest_framework import serializers

#2ta nokte:
#yeki inke esmeshun lazem nist mesle object bashe chon ye modele jodast (age esmo taqir bedim bayad tu source esme asli ro begim)
#2 inke faqat in 3ta field bar migardan az product
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_lenght=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)

```



## 9 Serializing Objects

```python
#un classe bala ro import mikonim v azash estefade mikonim.
@api_view()
def product_details(request, id):
    product = Product.objects.get(pk=id)
    serializer = ProductSerializer(product) 
    return Response(serializer.data)

#serializer.data dictionary bar migardune
```

vase inke not found dashte bashim:

```python
from rest_framework import status

@api_view()
def product_details(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

```

ama har seri bayad ino benevisim. ye rahe sade ine ke az __get_object_or_404__ tu frameworke django estefade konim.

```python
from django.shortcuts import get_list_or_404

@api_view()
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

```

vase getall:

```python
@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

#many=True vase ineke ma darim queryset besh midim v ba in migim bayad bere iterate kone v serialize kone.
```



## 10 Custom serializer fields

age bekhaym ye field dorost konim ke esmesh farq dare ba modelemun ya hata ye fielde jadid bashe bayad az serializerMethodField estefade konim:

```python
from rest_framework import serializers
from decimal import Decimal
from store.models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
# hame fielda source daran age bekhaym esm avaz konim
#1.1 floate bayad be decimal tabdilesh konim.
```



## 11 Serializing Relationships

```python
#rahe aval
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )
    
 #ye rahe dg inke tu apiemun biaym select_related konim collection ro bad be jaye primaryKeyRelatedField az StringRelatedField estefade konim ke be jaye id stringesho bar migardune(stringesh tu __str__ overide shode)
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    collection = serializers.StringRelatedField()
 
```



age bekhaym etelaate bishtari az relationemun ro neshun bedim bayad az un ye serialize object dorost konim bad tu un yeki model pass bedim:

```python
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collection = CollectionSerializer()

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

```

akharesham nahve estefade az hyperlink ro mige ke az khode video bbinim behtare.



## 12 Model Serializer

vase inke duplication beyne model v serializeremun nabashe az model serializer estefade mikonim. 

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'collection']
     	price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
 #tu fields migarde. age un esm tu model vojud dasht ke hamun ro serialize mikone. ama age vojud nadasht migarde tu hamin modelemun mesle qabl (mesle price)
```



## 13 Deserializing objects

aval inke tu python mishe ye method ro ham get ham post tarif kard (ke tu decorator tarif mishe). bad check konim vase har kodum chikar kone. vase deserialize kardanam:

```python
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        return Response('ok')
```



## 14 Validating Data

```python
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            return Response('ok')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
  #bakhshe elif tu code bala khodalse mishe be:
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response('ok')

```





## 15 Saving objects

vase save kardan mitunim az serialize.save() estefade konim. age bekhaym ye seri karaye dg anjam bedim mituni methode create v update ro override konim. ye mesal ham az update kardane paein miarim:

```python
@api_view(['GET', 'PUT'])
def product_detail(request, id):
    product = get_list_or_404(Product, pk=id)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

```



## 16 deleting objects

```python
@api_view(['DELETE'])
def product_detail(request, id):
    product = get_list_or_404(Product, pk=id)

    elif request.method == 'DELETE':
        product.delete()
        return response(status.HTTP_204_NO_CONTENT)

```





# Advanced API Concepts



## 2 Class Based Views

ta inja apihamun function base view budan ama ma class based view ham darim.

``` python
from rest_framework.views import APIView

class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
#tu urls ham bayad refrence ro ba in esm eslah konim v tahesh as_view() bezarim:
path('products/', views.ProductList.as_view()),
```



## 3 Mixins

ye classe tu rest_framework ke karaye crud ro piade sazi karde v niazi be baznevisi nist.



## 4 Generic Views

ye classe dg tu rest_framworde ke 1 2 ta az mixinis haro edqam karde v mitunim azashun estefade konim. vase estefade az in classa bayad az classi ke made nazaremune ersbari konim bad methodasho override konim:

```python
#code bala tabdil mishe be:

class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

```

hala in code ro mishe kholase tar kard. age logice khasi dashte bashim hamin raheshe ke logicemuno tu methoda biarim ama age bekhaym faqat class pas bedim ya expressione kami dashte bashim mesle in mitunim inaro be field pass bedim:

```python
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
	serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

```



nokte: age az in ravesh estefade kardim v tush ye data ro annotate karde bashim tu api postesh un field ro mikhad azamun. vase inkar tu serializer jaei ke darim field ro tarif mikonim bayad bezanim ke in field readonlye.



## 5 Customizing generic views

age ye chandta method hamun budan v yekish logic dasht mitunim faqat uni ke logic dare ro override konim,

age tu url.py ye path tarif karde budim ke fielde khasi begire vase inke gir nade ke pk bashe v ina un esmi ke vared kardim (mesle id) ro bayad tu lookup_field vared konim.

``` python
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return response(status.HTTP_204_NO_CONTENT)

```



## 6 ViewSets

age 2ta api dashte bashim ke queryset v serializeri ke migiran yeki bashe mitunim az __ModelViewSet__ estefade konim v bad ba routing be har kodum az apia route konim.

age ye api faqat karaye get dashte bashe v nakhaym write dashte bashim mitunim az __ReadOnlyModelViewSet__ estefade konim:

```python
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    lookup_field = 'id'

    def delete(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        if collection.products.count() > 0:
            return Response({'error': 'collection cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

```



## 7 Routers

tu rest_framework ye class darim be esme __SimpleRouter__ ke viewset ro migire v khodesh routing ro dorost mikone:

```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

```

ye __DefaultRouter__ ham darim ke 2ta chize ezafe dare, yeki inke mitunim url api haro bbinim age faqat esme app ro bezanim (http://.../store/), 2vom ham mitunim json ro az result begirim age bade esme url .json bezanim (http://.../store/products.json)



## 9 Nested Router

age urlemun tarkibi v tu dar tu bud vase generate kardanesh bayad az nested router estefade konim. vase inkar bayad aval package __drf-nested-routers__ ro nasb konim:

```python
pip install drf-nested-routers
```

tu classe routers hamun classaye simple v default ro darim. vase nested routing:

```python
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

urlpatterns = router.urls + products_router.urls
#ba in code alan apihaye products/1/reviews ya products/1/reviews/1 ro darim
```



hala farz konim mikhaym ye review create konim v id product ro az url begirim:

```python
#aval tu classe ReviewViewSet methode get_serializer_context bayad override beshe
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    
#bad tu classe ReviewSerializer bayad methode create ro override konim

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description', 'product']

    def create(self, validated_data):
        product_id = self.context['product_id']
        Review.objects.create(product_id=product_id, **validated_data)

```



## 10 Filtering

az query_params mitunim chizaei ke ba query string ersal mishan ro bekhunim

```python
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_queryset(self):
        query_set = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            query_set = query_set.filter(collection_id=collection_id)

        return query_set
```



## 11 Generic filtering

django ye package dare ke khodesh filtering ro anjam mide:

```python
pip install django-filter
```

```python
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection_id']
```

vase custom filtering __django filters__ ro search kon.



## 12 13 Searching & Sorting

```python
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id', 'unit_price']
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
```

14 pagination dar surate niaz 2bare bekhun.





# Shopping Cart Api

## 3

age bekhaym ye parimary_key guid dashte bashim:

```python
from uuid import uuid4

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

```

age bekhaym az relatione 2ta modele mokhtalef faqat yedune dashte bashim tu meta bayad az __unique_together__ estefade konim.

```python
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']] #list of list
```



## 4 

age ye api dashte bashim ke bazi az amaliataro nakhaym (masalan get all ro nakhaym) bayad az customViewSet estefade konim:

```python
#inja felan faqat create ro dare
class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

```



## 8

momkene tu ye viewset bekhaym az 2ta serializere mokhtalef estefade konim. vase inkar bayad methode __get_serializer_class__ ro tu viewset override konim:

```python
class CartItemViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer
```



age bekhaym methode save ro override konim bad az inke data validate shode bashe ma be __validated_data__ dastresi darim v mitunim azashun estefade konim:

```python
def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
```



bazi az value haei ke mikhaym momkene tu url bashan. vase estefade tu serializer aval bayad tu viewset az kwargs begirim v tu context pass bedim be serializer bad tu serializer az self.context begirimesh:

```python
#in view
def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
#in serializer
def save(self, **kwargs):
        cart_id = self.context['cart_id']

```

mesale override save:

```python
def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance
    
#tu piade sazie khode save akharesh che update bashe che create result ro tu self.instance mirize.
```



age bekhaym ye seri az fieldaye khas ke post mishan ro validate konim:

```python
#aval tu serializer ye method tarif mikonim:
def validate_product_id(self, value): #convention roayat she (daqiqan bayad avalesh validate bad esme field bashe badesh khodkar khodesh validation ro vase in field anjam mide)
    if not Product.objects.filter(pk=value).exists():
        raise serializers.ValidationError('message')
    return value
```



## 9 

tu viewset ye field dare ke mitunim noe request ro moshakhas konim.

```python
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
#dg put nemitune befreste
#bayad lowercase neveshte beshan
```



# Authentication System

## 2

__is_staff__ tu jadvale auth_user mige ke user mitune be panele admin dastresi dashte bashe ya na. 



## 3 customizing the user model

vase inkar 2 ta rah darim:

__1- Extend User__ - ye classe dg misazim ke az user ersbari kone. injur fieldash mire tu classe user

__2- Create Profile__ - ye model dg misazim ke az dariqe composition ba user ertebat dare. injuri ye table dg misaze ke foreign key dare ba user

hala age  bekhaym be authentication chizi ezafe konim bayad az raveshe aval estefade konim age ke rabti be authentication nadaran bayad az raveshe 2vom estefade konim.



## 4 Extending the user model

age bekhaym tu fieldaei ke hast taqir bedim bayad ye class dorost konim ke az __AbstractUser__

ersbari kone. 

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
```

bad bayad tu setting begim ke mikhaym az in classe jadid estefade konim.

```python
AUTH_USER_MODEL = 'core.User' #core esme applicationemune ke user tu classe un tarif shode
```

az inja be bad vase inke application vabaste be user nabashe nabayad mostaqim be user reference bedim. masalan:

```python
from django.conf import settings


class LikedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

```



dar edame ezafe kardan be admin ro mige.



## 5 User Profiles

model ro dorost mikonim v ye relatione oneToOne midim be user

```python
user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```



## 7 Custom Permissions

django khodesh tamame permissionaro vase api misaze. ama hamashun crudan. hala age bekhaym ye permissione khast khodemun ezafe konim bayad tu modelesh, tu classe meta ye field ezafe konim:

```python
   class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]
# ye list az tuple migire ke avali key hast 2vomi description
```



# Securing APIs



## 3 add authentication endpoints

django ye library dare be esme __Djoser__ ke vase karaye authentication view amade karde.



## 4 Registering Users

djoser ye seri api dare ke mesle panele admin mishe beshun dastresi dasht. hala age bekhaym model ro vase ye api avaz konim bayad ye seri taqirat bedim. masalan age vase methode create bekhaym modele user ro avaz konim ke fieldaye dg ham dashte bashe aval bayad berim tu documentation djoser tu bakhshe serializer hame serializeriaei ke dare estefade mikone ro neveshte. hala un chizi ke mikhaym taqir bedim ro ba modele khodemun jaygozin mikonim (tu settings):

(ye nokte inke in taqirat ro tu core app anjam midim chon vabaste be projan)

```python
#ye file jadid be esme serializer.py tu core
#classe UserCreateSerializer ro az documentation peyda kardim
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
```

bad in class ro tu setting proje ezafe mikonim:

```python
#key user_create ro az documentation peyda kardim
DJOSER = {
    'SERIALIZERS' : {
        'user_create': 'core.serializers.UserCreateSerializer'
    }
}
```

