from django.urls import path
from event_planning.views import EventPlanningCategoriesViewSet, EventPlanningSubCategoryViewSet
from categories.views import CategoryViewSet
from rent_hire.views import RentHireCategoryViewSet, RentHireSubCategoryViewSet
from store.views import StoreViewSet, OfferingViewSet, ReviewViewSet, StoreImageViewSet, ProvinceViewSet, AreaViewSet
from users.views import LoginView, MessageViewSet, LikeViewSet, LogoutView, RefreshTokenView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='api-refresh-token'),
    path('users/', UserViewSet.as_view({'get': 'list','post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='user-detail'),
    path('users/profile/', UserViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='user-detail'),

    # Phone Numbers
    # path('user/update-type/', UserTypeUpdateView.as_view({'patch': 'update'}), name='user-type-update'),
    
    # path('phone-numbers/', PhoneNumberView.as_view({'get': 'list', 'post': 'create'}), name='phone-number-list'),
    # path('phone-numbers/<int:pk>/', PhoneNumberView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='phone-number-detail'),

    # Event Planning Categories and Subcategories
    path('eventcategory/', EventPlanningCategoriesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('eventcategory/<int:pk>/', EventPlanningCategoriesViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
    path('eventsubcategory/', EventPlanningSubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('eventsubcategory/<int:pk>/', EventPlanningSubCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    # Rent & Hire Categories and Subcategories
    path('rentcategory/', RentHireCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('rentcategory/<int:pk>/', RentHireCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
    path('rentsubcategory/', RentHireSubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('rentsubcategory/<int:pk>/', RentHireSubCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    # General Categories
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Province and Area endpoints
    path('provinces/', ProvinceViewSet.as_view({'get': 'list'}), name='province-list'),
    path('provinces/<int:pk>/', ProvinceViewSet.as_view({'get': 'retrieve'}), name='province-detail'),
    path('areas/', AreaViewSet.as_view({'get': 'list'}), name='area-list'),
    path('areas/<int:pk>/', AreaViewSet.as_view({'get': 'retrieve'}), name='area-detail'),
    path('areas/by_province/', AreaViewSet.as_view({'get': 'by_province'}), name='areas-by-province'),

    # Store-related URLs
    path('stores/', StoreViewSet.as_view({'get': 'list', 'post': 'create'}), name='store-list'),
    path('stores/<int:pk>/', StoreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='store-detail'),
    path('stores/by_user/', StoreViewSet.as_view({'get': 'list_by_user'}), name='stores-by-user'),
    path('stores/search/', StoreViewSet.as_view({'get': 'search_stores'}), name='store-search'),

    # Store filtering endpoints
    path('stores/filter-by-category/<int:category_id>/', StoreViewSet.as_view({'get': 'filter_by_category'}), name='stores-filter-by-category'),
    path('stores/filter-by-location/<str:location>/', StoreViewSet.as_view({'get': 'filter_by_location'}), name='stores-filter-by-location'),

    # Reviews and offerings for a store
    path('store_list/<int:store_id>/reviews/', ReviewViewSet.as_view({'get': 'list_by_store'}), name='reviews_by_store'),
    path('store_list/<int:store_id>/offerings/', OfferingViewSet.as_view({'get': 'list_by_store'}), name='offerings_by_store'),

    # Consolidated Store Images endpoints
    path('store/<int:store_id>/images/', StoreImageViewSet.as_view({'get': 'list_by_store', 'post': 'create'}), name='store_images'),
    path('store/images/<int:pk>/', StoreImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='store_image_detail'),
    path('store/<int:store_id>/images/upload-multiple-images/', StoreImageViewSet.as_view({'post': 'upload_multiple'}), name='upload_multiple_images'),

    # User-related URLs
    # path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Messages and likes
    path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('likes/<int:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Reviews and offerings
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('offerings/', OfferingViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('offerings/<int:pk>/', OfferingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
]


# from django.urls import path
# from event_planning.views import EventPlanningCategoriesViewSet, EventPlanningSubCategoryViewSet
# from categories.views import CategoryViewSet
# from rent_hire.views import RentHireCategoryViewSet, RentHireSubCategoryViewSet
# from store.views import StoreViewSet, OfferingViewSet, ReviewViewSet, StoreImageViewSet
# from store.views import StoreViewSet, OfferingViewSet, ReviewViewSet, StoreImageViewSet  # Import the StoreImageViewSet
# from users.views import LoginView, MessageViewSet, LikeViewSet, LogoutView, RefreshTokenView, UserViewSet
# from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     # Authentication
#     path('login/', LoginView.as_view(), name='api-login'),
#     path('logout/', LogoutView.as_view(), name='api-logout'),
#     path('token/refresh/', RefreshTokenView.as_view(), name='api-refresh-token'),
#     path('users/', UserViewSet.as_view({'get': 'list','post': 'create'}), name='user-list'),
#     path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='user-detail'),
#     path('users/profile/', UserViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='user-detail'),

#     # Phone Numbers
#     # path('user/update-type/', UserTypeUpdateView.as_view({'patch': 'update'}), name='user-type-update'),
    
#     # path('phone-numbers/', PhoneNumberView.as_view({'get': 'list', 'post': 'create'}), name='phone-number-list'),
#     # path('phone-numbers/<int:pk>/', PhoneNumberView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='phone-number-detail'),

#     # Event Planning Categories and Subcategories
#     path('eventcategory/', EventPlanningCategoriesViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('eventcategory/<int:pk>/', EventPlanningCategoriesViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
#     path('eventsubcategory/', EventPlanningSubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('eventsubcategory/<int:pk>/', EventPlanningSubCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

# # Rent & Hire Categories and Subcategories
#     path('rentcategory/', RentHireCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('rentcategory/<int:pk>/', RentHireCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
#     path('rentsubcategory/', RentHireSubCategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('rentsubcategory/<int:pk>/', RentHireSubCategoryViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

#     # General Categories
#     path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

#     # Store-related URLs
#     path('stores/', StoreViewSet.as_view({'get': 'list', 'post': 'create'}), name='store-list'),
#     path('stores/<int:pk>/', StoreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='store-detail'),

#     # Store filtering endpoints
#     path('stores/filter-by-category/<int:category_id>/', StoreViewSet.as_view({'get': 'filter_by_category'}), name='stores-filter-by-category'),
#     path('stores/filter-by-location/<str:location>/', StoreViewSet.as_view({'get': 'filter_by_location'}), name='stores-filter-by-location'),

#     # Reviews and offerings for a store
#     path('store_list/<int:store_id>/reviews/', ReviewViewSet.as_view({'get': 'list_by_store'}), name='reviews_by_store'),
#     path('store_list/<int:store_id>/offerings/', OfferingViewSet.as_view({'get': 'list_by_store'}), name='offerings_by_store'),

#     # Consolidated Store Images endpoints
#     path('store/<int:store_id>/images/', StoreImageViewSet.as_view({'get': 'list_by_store', 'post': 'create'}), name='store_images'),
#     path('store/images/<int:pk>/', StoreImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='store_image_detail'),
#     path('store/<int:store_id>/images/upload-multiple-images/', StoreImageViewSet.as_view({'post': 'upload_multiple'}), name='upload_multiple_images'),

#     # User-related URLs
#     # path('users/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'})),
#     # path('users/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

#     # Messages and likes
#     path('messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('messages/<int:pk>/', MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
#     path('likes/', LikeViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('likes/<int:pk>/', LikeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

#     # Reviews and offerings
#     path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('reviews/<int:pk>/', ReviewViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
#     path('offerings/', OfferingViewSet.as_view({'get': 'list', 'post': 'create'})),
#     path('offerings/<int:pk>/', OfferingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
# ]