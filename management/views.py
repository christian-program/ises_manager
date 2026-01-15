import pandas as pd
import zipfile
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from portal.models import Post, StudentResult, Promotion, Department

# Sécurité : Vérifie si l'utilisateur est un membre du personnel (Enseignant/Admin)
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def teacher_dashboard(request):
    """Vue principale du tableau de bord enseignant."""
    return render(request, 'management/dashboard.html')

@login_required
@user_passes_test(is_staff)
def create_post(request):
    """Vue pour publier des posts, communiqués ou horaires."""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_type = request.POST.get('post_type')
        promotion_id = request.POST.get('promotion')
        
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        pdf = request.FILES.get('document_pdf')

        # Récupération de l'instance de Promotion si sélectionnée
        promotion_obj = None
        if promotion_id:
            promotion_obj = get_object_or_404(Promotion, id=promotion_id)

        # Création du post
        Post.objects.create(
            title=title,
            content=content,
            post_type=post_type,
            promotion=promotion_obj,
            image=image,
            video=video,
            document_pdf=pdf,
            author=request.user
        )
        return redirect('home')

    # On récupère toutes les promotions pour la liste déroulante du formulaire
    promotions = Promotion.objects.all().order_by('department__name', 'name')
    return render(request, 'management/create_post.html', {'promotions': promotions})

@login_required
@user_passes_test(is_staff)
def bulk_upload(request):
    """Vue pour l'importation massive des résultats (Excel + ZIP)."""
    if request.method == 'POST' and request.FILES.get('zip_file') and request.FILES.get('excel_file'):
        zip_file = request.FILES['zip_file']
        excel_file = request.FILES['excel_file']
        promotion_id = request.POST.get('promotion')
        
        promotion_obj = get_object_or_404(Promotion, id=promotion_id)
        
        # 1. Sauvegarde temporaire du ZIP
        fs = FileSystemStorage()
        zip_path = fs.save(f'temp_{zip_file.name}', zip_file)
        full_zip_path = os.path.join(settings.MEDIA_ROOT, zip_path)

        # 2. Lecture de l'Excel avec Pandas
        df = pd.read_excel(excel_file)

        # 3. Extraction et traitement du ZIP
        extract_path = os.path.join(settings.MEDIA_ROOT, 'temp_extracted')
        with zipfile.ZipFile(full_zip_path, 'r') as zref:
            zref.extractall(extract_path)

        # 4. Parcours de l'Excel et création des résultats
        # ... (début de la fonction bulk_upload identique) ...
        
        # 4. Parcours de l'Excel et création des résultats
        for index, row in df.iterrows():
            matricule = str(row['matricule']).strip() # .strip() pour enlever les espaces invisibles
            nom_etudiant = row['nom']
            nom_fichier_pdf = f"{matricule}.pdf"
            
            # CORRECTION : Recherche récursive du fichier dans tous les sous-dossiers
            pdf_source_path = None
            for root, dirs, files in os.walk(extract_path):
                if nom_fichier_pdf in files:
                    pdf_source_path = os.path.join(root, nom_fichier_pdf)
                    break

            # ... à l'intérieur de la boucle for dans bulk_upload ...
            if pdf_source_path and os.path.exists(pdf_source_path):
                with open(pdf_source_path, 'rb') as f:
                    from django.core.files import File
                    
                    # On ajoute 'author': request.user dans les defaults
                    resultat, created = StudentResult.objects.update_or_create(
                        student_id=matricule,
                        defaults={
                            'student_name': nom_etudiant,
                            'promotion': promotion_obj,
                            'author': request.user  # <--- AJOUTEZ CETTE LIGNE ICI
                        }
                    )
                    resultat.result_pdf.save(nom_fichier_pdf, File(f), save=True)
            else:
                print(f"⚠️ Fichier non trouvé pour : {nom_fichier_pdf}")

        # Nettoyage des fichiers temporaires
        os.remove(full_zip_path)
        # Note : En production, il faudrait aussi supprimer le dossier temp_extracted proprement

        return render(request, 'management/dashboard.html', {'message': 'Importation réussie !'})

    promotions = Promotion.objects.all().order_by('department__name', 'name')
    return render(request, 'management/bulk_upload.html', {'promotions': promotions})