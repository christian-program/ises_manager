
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='departments/', blank=True, null=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="promotions")

    def __str__(self):
        return f"{self.name} / {self.department.name}"

class Post(models.Model):
    POST_TYPES = (
        ('GENERAL', 'Publication Générale'),
        ('NEWS', 'Communiqué Officiel'),
        ('SCHEDULE', 'Horaire de Cours'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='GENERAL')
    title = models.CharField(max_length=200)
    content = models.TextField()
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    document_pdf = models.FileField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class StudentResult(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Ajoutez null=True
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=50, unique=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    result_pdf = models.FileField(upload_to='results_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)