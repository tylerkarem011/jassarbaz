from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

MEMBER_TYPE_CHOICES = [
    ('sarbaz', 'Сарбаз'),
    ('commander', 'Бөлімше командирі'),
]

class ClubMember(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    birth_date = models.DateField("Дата рождения")
    student_id = models.CharField("Жеке номер (JS-23-00157)", max_length=50, unique=True)
    group = models.CharField("Группа", max_length=20, default="MC-23-1")
    photo = models.ImageField("Фото", upload_to='photos/', null=True, blank=True)
    join_date = models.DateField("Дата вступления", default=timezone.now)
    is_active = models.BooleanField("Активен", default=True)
    score = models.PositiveIntegerField(default=0, verbose_name="Ұпай саны")

    # ==================== НАВЫКИ (1-5) ====================
    drill_score = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Саптық дайындық (1-5)"
    )
    shooting_score = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Атыс дайындығы (1-5)"
    )
    tactical_score = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Тактикалық дайындық (1-5)"
    )
    first_aid_score = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Алғашқы көмек (1-5)"
    )
    navigation_score = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Бағдарлау (1-5)"
    )
    patriotism_score = models.PositiveSmallIntegerField(
        default=1, 
        verbose_name="Патриотизм (1-5)"
    )
    # ====================================================

    @property
    def total_score(self):
        """Рейтинг считается автоматически из навыков в админке"""
        
        # Сумма всех навыков (каждый от 1 до 5)
        skill_sum = (
            getattr(self, 'drill_score', 0) +
            getattr(self, 'shooting_score', 0) +
            getattr(self, 'tactical_score', 0) +
            getattr(self, 'first_aid_score', 0) +
            getattr(self, 'navigation_score', 0) +
            getattr(self, 'patriotism_score', 0)
        )
        
        # Бонусы
        base = 300
        achievements_bonus = self.achievements.count() * 50 if hasattr(self, 'achievements') else 0
        commander_bonus = 200 if self.member_type == 'commander' else 0
        active_bonus = 100 if self.is_active else 0
        
        return base + skill_sum * 15 + achievements_bonus + commander_bonus + active_bonus

    member_type = models.CharField(
        max_length=20,
        choices=MEMBER_TYPE_CHOICES,
        default='sarbaz',
        verbose_name="Тип участника"
    )

    class Meta:
        ordering = ['-score']

    def get_member_type_display(self):
        return dict(MEMBER_TYPE_CHOICES).get(self.member_type, self.member_type)

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    SKILL_TYPES = [
        ('physical', 'Дене дайындығы'),
        ('shooting', 'Атыс дайындығы'),
        ('tactical', 'Тактикалық дайындық'),
        ('medical', 'Медициналық көмек'),
        ('patriot', 'Патриотизм және тәрбие'),
    ]

    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE, related_name='skills')
    skill_type = models.CharField("Тип навыка", max_length=20, choices=SKILL_TYPES)
    name = models.CharField("Название навыка", max_length=150)
    level = models.IntegerField("Уровень (1-5)", validators=[MinValueValidator(1), MaxValueValidator(5)])
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.member} - {self.name} ({self.level})"


class Achievement(models.Model):
    title = models.CharField("Атауы", max_length=200)
    description = models.TextField("Сипаттама", blank=True)
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE, related_name='achievements', verbose_name="Сарбаз")
    date = models.DateField("Күні", default=timezone.now)
    icon = models.CharField("Иконка (fa-...)", max_length=50, default="fa-trophy", help_text="Font Awesome иконкасы, мысалы: fa-medal, fa-trophy, fa-star")

    class Meta:
        verbose_name = "Жетістік"
        verbose_name_plural = "Жетістіктер"
        ordering = ['-date']

    def __str__(self):
        return f"{self.member.full_name} — {self.title}"


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Жоспарда'),
        ('done', 'Орындалды'),
    ]

    title = models.CharField("Название мероприятия", max_length=200)
    date = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True, verbose_name="Место проведения")
    is_completed = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        verbose_name="Статус"
    )

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField("Название", max_length=150)
    image = models.ImageField(upload_to='gallery/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField("Название видео", max_length=200)
    video_file = models.FileField("Видео файл", upload_to='videos/', null=True, blank=True)
    video_url = models.URLField("YouTube ссылка (опционально)", blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class Certificate(models.Model):
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE)
    title = models.CharField("Название сертификата", max_length=200)
    issue_date = models.DateField(default=timezone.now)
    pdf_file = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"Сертификат - {self.member}"
    
    
class Training(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Жоспарда'),
        ('ongoing', 'Жүріп жатыр'),
        ('completed', 'Аяқталды'),
    ]

    title = models.CharField("Атауы", max_length=200)
    description = models.TextField("Сипаттама", blank=True)
    date = models.DateTimeField("Күні мен уақыты")
    duration = models.PositiveIntegerField("Ұзақтығы (минут)", default=90)
    location = models.CharField("Өтетін жері", max_length=200, default="Спорт залы")
    instructor = models.CharField("Жаттықтырушы", max_length=100, default="Ахан А.Д.")
    max_participants = models.PositiveIntegerField("Максимум қатысушы", default=20)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='planned')
    photo = models.ImageField("Фото", upload_to='trainings/', null=True, blank=True)

    class Meta:
        verbose_name = "Жаттығу"
        verbose_name_plural = "Жаттығулар"
        ordering = ['-date']

    def __str__(self):
        return self.title 


class News(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'Жалпы'),
        ('training', 'Жаттығу'),
        ('achievement', 'Жетістік'),
        ('event', 'Іс-шара'),
    ]

    title = models.CharField("Тақырып", max_length=200)
    content = models.TextField("Мәтін")
    image = models.ImageField("Сурет", upload_to='news/', null=True, blank=True)
    category = models.CharField("Санат", max_length=20, choices=CATEGORY_CHOICES, default='general')
    date = models.DateTimeField("Жарияланған күні", default=timezone.now)
    is_published = models.BooleanField("Жарияланған", default=True)

    class Meta:
        verbose_name = "Жаңалық"
        verbose_name_plural = "Жаңалықтар"
        ordering = ['-date']

    def __str__(self):
        return self.title


     