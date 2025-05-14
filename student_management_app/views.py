import datetime
import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from student_management_app.models import Students, StudentResult,AttendanceReport
from django.db.models import Q


from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.models import CustomUser, Courses, SessionYearModel, Subjects , Staffs
from student_management_system import settings



def showDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response=requests.post(url=cap_url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)

        if cap_json['success']==False:
            messages.error(request,"Invalid Captcha Try Again")
            return HttpResponseRedirect("/")

        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    return render(request,"signup_admin_page.html")

def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})

def signup_staff(request):
    return render(request,"signup_staff_page.html")

def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    profile_pic = request.FILES['profile_pic']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)

    #try:
    user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                          first_name=first_name, user_type=3)
    user.students.address = address
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.object.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
    #except:
     #   messages.error(request, "Failed to Add Student")
      #  return HttpResponseRedirect(reverse("show_login"))



@csrf_exempt
def student_chatbot_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({"reply": "Authentification requise. Connectez-vous d'abord."})

    try:
        student = Students.objects.get(admin=request.user)
    except Students.DoesNotExist:
        return JsonResponse({"reply": "Profil étudiant introuvable."})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("message", "").strip().lower()

            # Accueil / salutation
            if any(mot in prompt for mot in ["bonjour", "salut", "hello", "coucou"]):
                return JsonResponse({
                    "reply": f"Bonjour {student.admin.first_name} ! Comment puis-je t'aider aujourd'hui ?",
                    "quick_replies": ["Mes absences", "Mes notes", "Aide en Java", "Aide en Python"]
                })

            # Gestion des absences
            if "absence" in prompt:
                subject = detect_subject(prompt, student)
                if subject:
                    absences = AttendanceReport.objects.filter(
                        student_id=student,
                        attendance_id__subject_id__subject_name__icontains=subject,
                        status=False
                    ).count()

                    if absences < 3:
                        return JsonResponse({
                            "reply": f"⚠️ Tu as été absent à {absences} séance(s) de {subject.upper()}."
                        })
                    else:
                        try:
                            result = StudentResult.objects.get(
                                student_id=student,
                                subject_id__subject_name__icontains=subject
                            )
                            note = result.subject_exam_marks
                        except StudentResult.DoesNotExist:
                            note = "N/A"

                        ai_prompt = (
                            f"Pour la matière {subject}, effectue ces étapes :\n"
                            f"1. Recherhe ACTUELLEMENT sur YouTube un tutoriel (filtre : publié <6 mois, >10k vues)\n"
                            f"2. Trouve un cours Udemy/OpenClassrooms avec au moins 4 étoiles\n"
                            f"3. Vérifie que les pages existent en accédant aux URLs\n"
                            f"4. Fournis UNIQUEMENT si tu as trouvé :\n"
                            f"   a) [VIDÉO] Titre exact (durée, niveau) : URL_complète\n"
                            f"   b) [COURS] Titre exact (prix/nbheures) : URL_complète\n"
                            f"5. Si rien de vérifiable : 'Aucune ressource fiable trouvée pour {subject}'\n\n"
                            f"Exemple de réponse VALIDE :\n"
                            f"[VIDÉO] Apprendre {subject} - Tutoriel 2024 (2h, débutant) : https://youtu.be/12345\n"
                            f"[COURS] {subject} avancé sur Udemy (19.99€, 8h) : https://www.udemy.com/course123"
                        )

                        headers = {
                            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        }
                        payload = {
                            "model": "mistralai/mistral-7b-instruct",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "Tu es un assistant pédagogique intelligent. Propose des ressources concrètes pour progresser (liens vidéos, forums) et un encouragement. Réponds en français, 4 lignes max."
                                },
                                {"role": "user", "content": ai_prompt}
                            ]
                        }

                        response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            json=payload,
                            timeout=10
                        )
                        ai_reply = response.json()["choices"][0]["message"]["content"]

                        final_reply = (
                            f"⚠️ Tu as {absences} absences en {subject.upper()} et ta note est {note}.\n\n"
                            f"{ai_reply}"
                        )
                        return JsonResponse({"reply": final_reply})
                else:
                    return JsonResponse({"reply": "Pour quelle matière veux-tu connaître tes absences ?"})

            # Gestion des notes
            if "note" in prompt or "resultat" in prompt:
                subject = detect_subject(prompt, student)
                if subject:
                    try:
                        result = StudentResult.objects.get(
                            student_id=student,
                            subject_id__subject_name__icontains=subject
                        )
                        note = result.subject_exam_marks

                        if note >= 12:
                            return JsonResponse({
                                "reply": f"✅ Ta note en {subject.upper()} est {note}/20. Très bon travail, continue comme ça !"
                            })
                        else:
                            ai_prompt = (
                                f"Un étudiant a eu {note}/20 en {subject}. "
                                f"Propose-lui des ressources adaptées à son niveau pour l'aider à progresser : vidéos YouTube, "
                                f"cours en ligne gratuits ou payants (OpenClassrooms, Udemy...) avec un lien de vidéo réel, pas généré. "
                                f"Ne dépasse pas 6 lignes. Termine par un message de motivation."
                            )

                            headers = {
                                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                                "Content-Type": "application/json"
                            }
                            payload = {
                                "model": "mistralai/mistral-7b-instruct",
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "Tu es un assistant pédagogique intelligent. Tu proposes aux étudiants en difficulté des ressources concrètes pour progresser (liens vidéos, cours) et un encouragement. Réponds en français, en 6 lignes maximum."
                                    },
                                    {"role": "user", "content": ai_prompt}
                                ]
                            }

                            response = requests.post(
                                "https://openrouter.ai/api/v1/chat/completions",
                                headers=headers,
                                json=payload,
                                timeout=10
                            )
                            ai_reply = response.json()["choices"][0]["message"]["content"]
                            final_reply = f"Ta note en {subject.upper()} est {note}/20.\n\n{ai_reply}"
                            return JsonResponse({"reply": final_reply})

                    except StudentResult.DoesNotExist:
                        return JsonResponse({"reply": f"Aucune note trouvée pour {subject.upper()}."})
                else:
                    return JsonResponse({"reply": "Pour quelle matière veux-tu connaître ta note ?"})
                
            # Interaction sociale et motivation
            if any(mot in prompt for mot in ["astuce", "conseil moi", "gerer mon temps", "organisation", "productivite"]) and "temps" in prompt:
                
                astuce_temps_prompt = (
                    "Donne une astuce simple et efficace à un étudiant pour mieux gérer son temps pendant les périodes de révisions. "
                    "Style amical, réponse courte (2 à 3 phrases), avec une méthode concrète à appliquer dès aujourd'hui. En français."
                )

                payload = {
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "Tu es un coach de productivité pour étudiants."},
                        {"role": "user", "content": astuce_temps_prompt}
                    ]
                }

                headers = {
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                ai_reply = response.json()["choices"][0]["message"]["content"]
                return JsonResponse({"reply": ai_reply})

            #motivation
            if any(mot in prompt for mot in ["motivation","motive" ,"examen", "examens", "encourage moi"]):
                motivation_exam_prompt = (
                    "Un étudiant stressé approche des examens. Écris un message motivant pour l’encourager. "
                    "Sois bienveillant, positif et inspirant. En français, maximum 3 phrases. Termine par une phrase de confiance."
                )

                payload = {
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "Tu es un coach motivant pour les étudiants."},
                        {"role": "user", "content": motivation_exam_prompt}
                    ]
                }

                headers = {
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                ai_reply = response.json()["choices"][0]["message"]["content"]
                return JsonResponse({"reply": ai_reply})

            # Orientation académique
            if "orientation" in prompt or "matiere" in prompt or "oriente" in prompt:
                results = StudentResult.objects.filter(student_id=student)
                if not results.exists():
                    return JsonResponse({"reply": "Je n'ai trouvé aucun résultat pour vous orienter."})

                notes_summary = "\n".join(
                    f"- {res.subject_id.subject_name}: {res.subject_exam_marks}/20"
                    for res in results
                )

                orientation_prompt = (
                    f"Voici les notes de l'étudiant :\n{notes_summary}\n\n"
                    f"L'étudiant demande des conseils d'orientation pour le semestre prochain. "
                    f"Donne-lui quelques conseils d'orientation à partir de ses notes qui vont l'aider, tu vas luis conseiller de s'orienter plus sur les matiere ou sa note est superieur a 12"
                )

                headers = {
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                            "model": "mistralai/mistral-7b-instruct",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "Tu es un assistant pédagogique intelligent. Propose des ressources concrètes pour progresser (liens vidéos, forums) et un encouragement. Réponds en français, 4 lignes max."
                                },
                                {"role": "user", "content": orientation_prompt}
                            ]
                        }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                ai_reply = response.json()["choices"][0]["message"]["content"]
                return JsonResponse({"reply": ai_reply})

            # Réponse IA par défaut
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://yourdomain.com",
                "X-Title": "Student Assistant",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-ai/deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un assistant pédagogique. Réponds en français de manière concise."
                    },
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10
            )
            return JsonResponse({"reply": response.json()["choices"][0]["message"]["content"]})

        except Exception as e:
            return JsonResponse({"reply": "Désolé, une erreur est survenue. Veuillez réessayer."})

    return JsonResponse({"reply": "Veuillez envoyer votre message via une requête POST."})

def detect_subject(prompt, student):
    """Détecte les matières à partir du prompt et vérifie qu'elles existent dans la base de données"""
    # Récupère toutes les matières de l'étudiant
    student_subjects = StudentResult.objects.filter(
        student_id=student
    ).values_list('subject_id__subject_name', flat=True).distinct()

    # Convertit en noms normalisés (minuscules)
    available_subjects = [s.lower() for s in student_subjects]

    # Vérifie chaque mot du prompt
    for word in prompt.split():
        word = word.lower().strip()
        # Vérifie si le mot correspond à une matière de l'étudiant
        for subject in available_subjects:
            if word in subject.lower():
                return subject  

    return None