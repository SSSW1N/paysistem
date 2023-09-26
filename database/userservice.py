from datetime import datetime
from database import get_db
from database.models import User, BlockedUser
from user import UserRegisterModel

# Регистрация пользователя
def register_user_db(new_data: UserRegisterModel):
    db = next(get_db())

    # Переводим все данные из пайдентика на словарь
    user_data = new_data.model_dump()
    new_user = User(**user_data)

    db.add(new_user)
    db.commit()

    return new_user

# Проверка на наличие пользователя
def chek_user_db(phone_number: int, password: str = None):
    db = next(get_db())

    cheker = db.query(User).filter_by(phone_number=phone_number).first()

    if cheker:
        if cheker.password == password:
            return cheker
        elif cheker.password != password:
            return 'Неверный пароль'

    return False


# Добавление фото пользователя
def add_profile_photo_db(user_id: int, photo_file_name: str):
    db = next(get_db())

    cheker = db.query(User).filter_by(id=user_id).first()

    if cheker:
        cheker.profile_photo = photo_file_name
        db.commit()

        return 'Фото успешно добавлен'

    return 'Профиль не найден'


# Изменить информацию о пользователе
def change_user_info_db(user_id: int, info_to_change: str, new_info: str):
    db = next(get_db())

    cheker = db.query(User).filter_by(id=user_id).first()

    if cheker:
        if info_to_change == 'new_password':
            cheker.password = new_info

        elif info_to_change == 'new_email':
            cheker.email = new_info

        elif info_to_change == 'new_city':
            cheker.city = new_info

        db.commit()

        return f'{info_to_change} изменен'

    return 'Не найден'


# Заблокировать пользователя
def block_user_db(user_id: int):
    db = next(get_db())

    cheker = db.query(BlockedUser).filter_by(user_id=user_id).first()

    if cheker:
        return True

    new_blocked_user = BlockedUser(user_id=user_id, blocked_date=datetime.now())
    db.add(new_blocked_user)
    db.commit()

    return 'Заблокирован'


# Разблокировать пользователя
def unblock_user_db(user_id: int):
    db = next(get_db())

    cheker = db.query(BlockedUser).filter_by(user_id=user_id).first()

    if cheker:
        db.delete(cheker)
        db.commit()

        return 'Разблокирован'

    return 'Не найдено'

