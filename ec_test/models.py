from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator

# Create your models here.


# 作品の画像
class ItemImage(models.Model):

    origin = models.ImageField(upload_to="photos/%y/%m/%d/")

    big = ImageSpecField(source="origin",
                         processors=[ResizeToFill(1280, 1024)],
                         format='JPEG'
                         )

    thumbnail = ImageSpecField(source='origin',
                               processors=[ResizeToFill(250, 250)],
                               format="JPEG",
                               options={'quality': 60}
                               )

    middle = ImageSpecField(source='origin',
                            processors=[ResizeToFill(600, 400)],
                            format="JPEG",
                            options={'quality': 75}
                            )

    small = ImageSpecField(source='origin',
                           processors=[ResizeToFill(75, 75)],
                           format="JPEG",
                           options={'quality': 50}
                           )


# 作者テーブル
class Author(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


# 商品テーブル
class Merchandise(models.Model):
    price = models.PositiveIntegerField(verbose_name='本体価格')
    # postage = models.PositiveIntegerField(verbose_name='送料')  # 0円もOK
    size_d = models.PositiveIntegerField(verbose_name='奥行き')  # サイズは送料を計算するときに使う
    size_l = models.PositiveIntegerField(verbose_name='幅')
    size_h = models.PositiveIntegerField(verbose_name='高さ')
    name = models.CharField(max_length=200, verbose_name='商品名')
    description = models.CharField(max_length=500, verbose_name='説明')
    image = models.ForeignKey(to=ItemImage, on_delete=models.CASCADE, related_name='merchandise')
    author = models.ForeignKey(to=Author, on_delete=models.PROTECT, blank=True, null=True, related_name='items')  # 作者
    on_sale = models.BooleanField(verbose_name='販売中', default=True)
    soled_amount = models.PositiveIntegerField(verbose_name='販売個数', default=0)  # 今までの売れた合計の個数

    def __str__(self):
        return self.name


# お客様情報
class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='氏名')
    hurigana = models.CharField(max_length=100, verbose_name='フリガナ')
    mail_address = models.CharField(max_length=256, verbose_name='メールアドレス')  # 最大のメールアドレスの長さが256文字まで
    address = models.CharField(max_length=200, verbose_name='住所')
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message=(
        "Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))  # validator
    phone_number = models.CharField(validators=[tel_number_regex], max_length=15, verbose_name='電話番号')
    gender = models.BooleanField(verbose_name='性別', choices=((True, '男'), (False, '女')), blank=True, null=True)
    password = models.CharField(max_length=128, verbose_name='パスワード')

    def __str__(self):
        return self.name


# 注文テーブル
class Order(models.Model):
    number = models.IntegerField()
    total_price = models.PositiveIntegerField(verbose_name='合計金額')
    postage = models.PositiveIntegerField(verbose_name='送料')  # 合計金額のうちの送料分
    accept_choices = ((0, '宅配'), (1, '取りに来る'))
    payment_choices = ((0, '現金'), (1, 'カード'))
    acceptance = models.PositiveSmallIntegerField(choices=accept_choices, verbose_name='受け取り方法')
    payment = models.PositiveIntegerField(choices=payment_choices, verbose_name='支払い方法')
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='order_history')
    created_at = models.DateTimeField(verbose_name='注文日時')
    dead_line = models.DateField(verbose_name='納期')
    start_delivery = models.DateTimeField(verbose_name='配送開始日時', null=True, blank=True)
    delivered = models.DateTimeField(verbose_name='取引完了日時')

    def __str__(self):
        return ' '.join([str(self.customer), str(self.created_at)])  # 注文者 + 注文日時


# 注文のうちの各商品テーブル
class OrderDetail(models.Model):
    item = models.ForeignKey(to=Merchandise, on_delete=models.PROTECT, verbose_name='商品')
    quantity = models.SmallIntegerField(verbose_name='注文個数')
    price = models.PositiveIntegerField(verbose_name='商品ごと小計')
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='detail')

