from django.contrib import admin
from .models import Department, Promotion, Post, StudentResult, Comment

# Configuration de l'affichage des Départements
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Configuration des Promotions (avec filtre par département)
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

# Configuration des Résultats (pour voir qui appartient à quelle promo)
@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_id', 'get_promotion_name', 'get_dept_name')
    search_fields = ('student_name', 'student_id')
    list_filter = ('promotion__department', 'promotion')

    # Fonctions pour afficher les noms liés dans la liste
    def get_promotion_name(self, obj):
        return obj.promotion.name
    get_promotion_name.short_description = 'Promotion'

    def get_dept_name(self, obj):
        return obj.promotion.department.name
    get_dept_name.short_description = 'Département'

# Configuration des Posts
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_type', 'promotion', 'author', 'created_at')
    list_filter = ('post_type', 'promotion', 'created_at')
    search_fields = ('title', 'content')

# Commentaires
admin.site.register(Comment)