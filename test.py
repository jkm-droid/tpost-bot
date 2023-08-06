from configs.database import create_db_connection
from services import media_service

if __name__ == "__main__":
    db_connection = create_db_connection()
    slogan = media_service.get_slogan(db_connection)
    imag = media_service.add_slogan_on_image(db_connection)
    print(imag)
