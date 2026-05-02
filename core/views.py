from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
import io
from reportlab.lib.colors import HexColor
from django.db.models import Avg

from .models import ClubMember, GalleryImage, Event, Video, Achievement, Training, News
from .forms import ClubMemberForm

def dashboard(request):
    total = ClubMember.objects.count()
    active = ClubMember.objects.filter(is_active=True).count()
    
    context = {
        'total_members': total,
        'active_members': active,
        'avg_drill': round(ClubMember.objects.aggregate(Avg('drill_score'))['drill_score__avg'] or 4) * 20,
        'avg_shooting': round(ClubMember.objects.aggregate(Avg('shooting_score'))['shooting_score__avg'] or 4) * 20,
        'avg_tactical': round(ClubMember.objects.aggregate(Avg('tactical_score'))['tactical_score__avg'] or 4) * 20,
        'avg_first_aid': round(ClubMember.objects.aggregate(Avg('first_aid_score'))['first_aid_score__avg'] or 4) * 20,
        'avg_navigation': round(ClubMember.objects.aggregate(Avg('navigation_score'))['navigation_score__avg'] or 4) * 20,
        'avg_patriotism': round(ClubMember.objects.aggregate(Avg('patriotism_score'))['patriotism_score__avg'] or 4) * 20,
    }
    return render(request, 'core/dashboard.html', context)

def member_list(request):
    members = ClubMember.objects.all().order_by('-join_date')
    return render(request, 'core/member_list.html', {'members': members})


def member_detail(request, pk):
    member = get_object_or_404(ClubMember, pk=pk)
    skills = member.skills.all()
    achievements = member.achievements.all()
    return render(request, 'core/member_detail.html', {
        'member': member,
        'skills': skills,
        'achievements': achievements,
    })


def generate_certificate(request, member_id):
    from .models import ClubMember
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from datetime import date
    import qrcode
    from io import BytesIO

    member = get_object_or_404(ClubMember, id=member_id)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Шрифты
    try:
        pdfmetrics.registerFont(TTFont('DejaVu', 'static/fonts/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuBold', 'static/fonts/DejaVuSans-Bold.ttf'))
        font_name = 'DejaVu'
        font_bold = 'DejaVuBold'
    except:
        font_name = 'Helvetica'
        font_bold = 'Helvetica-Bold'

    # === ФОН ===
    p.setFillColor(HexColor("#ffffff"))
    p.rect(0, 0, width, height, fill=1, stroke=0)

    # === ЛОГО СЛЕВА ===
    try:
        logo_left = ImageReader("static/images/logo2.png")
        p.drawImage(logo_left, 25, height - 100, width=100, height=80, 
                    preserveAspectRatio=True, mask='auto')
    except:
        pass

    # === ЗАГОЛОВОК ===
    p.setFillColor(HexColor("#0d6efd"))
    p.setFont(font_bold, 30)
    p.drawCentredString(width/2, height - 50, "ДИПЛОМ")

    p.setFont(font_bold, 12)
    p.setFillColor(HexColor("#003087"))
    p.drawCentredString(width/2, height - 73, "ЖАС САРБАЗ ӘСКЕРИ-ПАТРИОТТЫҚ КЛУБЫ")

    # === БЕЙДЖ СПРАВА ===
    try:
        logo_right = ImageReader("static/images/лого2.png")
        p.drawImage(logo_right, width - 100, height - 100, width=80, height=75, 
                    preserveAspectRatio=True, mask='auto')
    except:
        pass
    # === ФОТО ===
    if member.photo:
        try:
            photo = ImageReader(member.photo.path)
            p.drawImage(photo, 35, height - 290, width=130, height=170, preserveAspectRatio=True, mask='auto')
        except:
            pass

    # === ФИО ===
    p.setFillColor(HexColor("#003087"))
    p.setFont(font_bold, 17)
    p.drawCentredString(width/2 + 25, height - 160, member.full_name.upper())

    p.setFont(font_name, 10)
    p.setFillColor(HexColor("#555555"))
    p.drawCentredString(width/2 + 25, height - 178, f"Тобы: {member.group}  •  Туған күні: {member.birth_date}")

    # === НАВЫКИ (реальные данные) ===
    y = height - 365
    p.setFillColor(HexColor("#0d6efd"))
    p.roundRect(35, y - 5, width - 70, 22, 5, fill=1, stroke=0)
    p.setFillColor(HexColor("#ffffff"))
    p.setFont(font_bold, 10)
    p.drawCentredString(width/2, y + 2, "ДАҒДЫЛАР ПАСПОРТЫ (SKILLS PASSPORT)")

    y -= 58
    skills = [
        ("Дене дайындығы", member.drill_score * 20),
        ("Атыс дайындығы", member.shooting_score * 20),
        ("Саптық дайындық", member.drill_score * 20),
        ("Тактикалық дайындық", member.tactical_score * 20),
        ("Медициналық көмек", member.first_aid_score * 20),
        ("Патриотизм", member.patriotism_score * 20),
    ]

    for name, level in skills:
        p.setFont(font_name, 8.5)
        p.setFillColor(HexColor("#333333"))
        p.drawString(45, y, name)

        p.setFillColor(HexColor("#e9ecef"))
        p.roundRect(200, y - 2, 230, 14, 4, fill=1, stroke=0)
        p.setFillColor(HexColor("#0d6efd"))
        p.roundRect(200, y - 2, 230 * (level / 100), 14, 4, fill=1, stroke=0)
        p.setFont(font_bold, 7.5)
        p.setFillColor(HexColor("#ffffff"))
        p.drawString(207, y + 1, f"{level}%")
        y -= 19

    # === ЖЕТІСТІКТЕР (реальные данные участника) ===
    y -= 70
    p.setFillColor(HexColor("#0d6efd"))
    p.roundRect(35, y - 5, width - 70, 22, 5, fill=1, stroke=0)
    p.setFillColor(HexColor("#ffffff"))
    p.setFont(font_bold, 10)
    p.drawCentredString(width/2, y + 2, "ЖЕТІСТІКТЕРІ")

    y -= 30
    p.setFillColor(HexColor("#333333"))
    p.setFont(font_name, 9)

    # Реальные достижения на основе оценок
    achievements = []
    
    if member.drill_score >= 4:
        achievements.append("★ Саптық дайындық бойынша үздік")
    if member.shooting_score >= 4:
        achievements.append("★ Атыс дайындығы бойынша үздік")
    if member.tactical_score >= 4:
        achievements.append("★ Тактикалық дайындық бойынша үздік")
    if member.first_aid_score >= 4:
        achievements.append("★ Алғашқы көмек бойынша үздік")
    if member.navigation_score >= 4:
        achievements.append("★ Бағдарлау бойынша үздік")
    if member.patriotism_score >= 4:
        achievements.append("★ Патриотизм бойынша үздік")

    # Если мало достижений — показываем текущие оценки
    if len(achievements) < 3:
        achievements = [
            f"★ Саптық дайындық — {member.drill_score}/5",
            f"★ Атыс дайындығы — {member.shooting_score}/5",
            f"★ Тактикалық дайындық — {member.tactical_score}/5",
        ]

    for ach in achievements[:5]:  # максимум 5 достижений
        p.drawString(50, y, ach)
        y -= 16

    # === ПОДПИСЬ ===
    p.setFont(font_name, 9)
    p.setFillColor(HexColor("#333333"))
    p.drawString(45, 82, "Клуб жетекшісі: Ахан А.Д.")

    # === ТЕКУЩАЯ ДАТА (сегодняшний день) ===
    today = date.today().strftime("%d.%m.%Y")
    p.drawString(45, 66, f"Берілген күні: {today}")

    # === ДЕВИЗ ===
    p.setFont(font_name, 7.5)
    p.drawCentredString(width/2, 42, "«ОТАНҒА ДЕГЕН СҮЙІСПЕНШІЛІК – ЕЛГЕ ҚЫЗМЕТ ЕТУДЕН БАСТАЛАДЫ!»")

    # === COPYRIGHT ===
    p.setFillColor(HexColor("#6c757d"))
    p.setFont(font_name, 6.5)
    p.drawCentredString(width/2, 18, 
        "Innovative Technical College Jas Sarbaz, all rights reserved 2026")

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{member.full_name}_jas_sarbaz_diplom.pdf"'
    return response

def gallery(request):
    images = GalleryImage.objects.all().order_by('-upload_date')
    return render(request, 'core/gallery.html', {'images': images})


def events(request):
    events_list = Event.objects.all().order_by('date')
    return render(request, 'core/events.html', {'events': events_list})


def videos(request):
    from .models import Video
    video_list = Video.objects.all().order_by('-upload_date')
    return render(request, 'core/videos.html', {'videos': video_list})

def news(request):
    news_list = News.objects.filter(is_published=True).order_by('-date')
    return render(request, 'core/news.html', {'news_list': news_list})

def trainings(request):
    trainings = Training.objects.all().order_by('-date')
    return render(request, 'core/trainings.html', {'trainings': trainings})

def achievements(request):
    achievements = Achievement.objects.select_related('member').all()
    return render(request, 'core/achievements.html', {'achievements': achievements})

def rating(request):
    from .models import ClubMember
    
    members = list(ClubMember.objects.all())
    members.sort(key=lambda m: m.total_score, reverse=True)
    
    return render(request, 'core/rating.html', {'members': members})

def leadership(request):
    return render(request, 'core/leadership.html')

def join(request):
    return render(request, 'core/join.html')