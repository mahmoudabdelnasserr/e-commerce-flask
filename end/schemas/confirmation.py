from ma import ma
from models.confirmation import ConfirmationModel


class ConfirmationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id", "expired_at", "confirmed")
        include_fk = True
