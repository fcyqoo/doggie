from django.db import models

# Create your models here.


class DogBase(models.Model):
    # This is the source key of the asset, NOT content key
    dog_name_id = models.CharField(max_length=32, null=False, blank=False)  # 逻辑外键
    dog_name = models.CharField(max_length=32, null=True, blank=True)
    dog_type = models.CharField(max_length=16, null=True, blank=True)
    dog_size = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        db_table = 'dog_base'


class DogDetail(models.Model):
    dog_name_id = models.CharField(max_length=32, null=False, blank=False)  # 逻辑外键
    part = models.CharField(max_length=16, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'dog_detail'


class DogInfo(models.Model):
    dog_name_id = models.CharField(max_length=32, null=False, blank=False)  # 逻辑外键
    chinese_name = models.CharField(max_length=16, null=True, blank=True)
    english_name = models.CharField(max_length=64, null=True, blank=True)
    other_name = models.CharField(max_length=32, null=True, blank=True)
    homeland = models.CharField(max_length=32, null=True, blank=True)
    dog_size = models.CharField(max_length=16, null=True, blank=True)
    dog_color = models.CharField(max_length=16, null=True, blank=True)
    dog_type = models.CharField(max_length=16, null=True, blank=True)
    dog_image_url = models.CharField(max_length=100, null=True, blank=True)
    dog_personality = models.CharField(max_length=64, null=True, blank=True)
    dog_description = models.TextField(null=True, blank=True)
    dog_age_min = models.IntegerField(null=True, blank=True, default=None)
    dog_age_max = models.IntegerField(null=True, blank=True, default=None)
    dog_price_refer = models.CharField(max_length=16, null=True, blank=True, default=None)

    class Meta:
        db_table = 'dog_info'


class DogRaise(models.Model):
    dog_name_id = models.CharField(max_length=32, null=False, blank=False)  # 逻辑外键
    feed_description = models.TextField(null=True, blank=True)
    physiological_index = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'dog_raise'


class DogStar(models.Model):
    dog_name_id = models.CharField(max_length=32, null=True, blank=True)
    star_id = models.CharField(max_length=32, null=True, blank=True)
    start_picture = models.CharField(max_length=100, null=True, blank=True)
    chinese_name = models.CharField(max_length=16, null=True, blank=True)
    english_name = models.CharField(max_length=16, null=True, blank=True)
    birthday = models.DateField(null=True, default=None)
    date_of_death = models.DateField(null=True, default=None)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'dog_star'
