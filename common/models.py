from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 시간
    updated_at = models.DateTimeField(auto_now=True)  # 데이터가 업데이트 된 시간
    deleted_at = models.DateTimeField(
        null=True, blank=True, default=None
    )  # 데이터가 삭제된 시간(실제 테이블에서 삭제x)

    class Meta:
        abstract = True  # DB에 테이블을 추가하지 마세요.
