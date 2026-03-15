from django.db import models
from datetime import date
from django.core.validators import RegexValidator

# Create your models here.
phone_validator = RegexValidator(
    regex = r'^07\d{8}$',
    message = "Phone number must be in format 07XX XXX XXX."

)
id_validator = RegexValidator(
    regex=r'^\d{7,8}$',
    message = "Incorrect ID number format."
)
class Coach(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10,validators=[phone_validator])
    id_no = models.CharField(max_length=8,validators=[id_validator])
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
    
    def __str__(self):
        return {self.name}
    

class Position(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('RB', 'Right Back'),
        ('LB', 'Left Back'),
        ('DMF', 'Defensive Midfielder'),
        ('CMF', 'Center Midfielder'),
        ('AMF', 'Attacking Midfielder'),
        ('SS', 'Second Striker'),
        ('CF', 'Centre Forward'),
    ]
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)

    def __str__(self):
        return self.get_position_display()
    
class Skills(models.Model):
    DEFENSIVE_SKILLS = [
    ('ACROBATIC_CLEARANCES', 'Acrobatic Clearances'),
    ('SLIDING_TACKLE', 'Sliding Tackle'),
    ('STANDING_TACKLE', 'Sanding Tackle'),
    ('HEADING', 'Heading'),
    ('SUPER_JUMP', 'Super Jump'),
    ]

    ATTACKING_SKILLS = [
        ('BULLET_HEADER', 'Bullet Header'),
        ('BLITZ_CURL', 'Blitz Curl'),
        ('EDGED_CROSSING', 'Edged Crossing'),
        ('OUTSIDE_CURL', 'Outside Curl'),
        ('CHIP_SHOT', 'Chip Shot'),
    ]

    PLAYER_SKILLS = DEFENSIVE_SKILLS + ATTACKING_SKILLS

    skills = models.CharField(max_length=30, choices=PLAYER_SKILLS)

    def __str__(self):
        return self.get_skill_display()
    
class Club(models.Model):
    name = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
 
    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name
    
class Contract(models.Model):
    contract_start = models.DateField()
    contract_end = models.DateField()

    def __str__(self):
        return f'{self.contract_start} | {self.contract_end}'
    
class Player(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10, validators=[phone_validator])
    id_no = models.CharField(max_length=8, validators=[id_validator], blank=True)
    skills = models.ManyToManyField(Skills)
    coach = models.ForeignKey(Coach, on_delete=models.SET)
    player_position = models.ManyToManyField(Position)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    club_before = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name="previous_players")
    current_club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name='current_players')
    created_at = models.DateTimeField(auto_now_add=True)

    class Activity(models.TextChoices):
        BENCH = "BENCH", "Bench"
        SUB = "SUBSTITUTE", "Substitute"
        STARTING = "STARTING_11", "Starting_11"

    activity = models.CharField(choices=Activity.choices)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} | {self.get_acitivity_display()}"

