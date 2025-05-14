import os.path

from dotenv import load_dotenv


class Config:

    def __init__(self):
        self.path: str = os.path.abspath('')  # Absolute path to our project

        load_dotenv()
        self.DSN: str = os.getenv("DSN")
        self.TOKEN: str = os.getenv("TOKEN")
        self.admins_ids: list[int] = [int(admin_id) for admin_id in (os.getenv("MANAGERS")).split('/') if admin_id]

    async def get_views(self) -> list[int]:
        """[views, full_form]"""
        with open(f"{self.path}/app/views.txt", encoding="utf-8") as file:
            data = [int(val.rstrip('\n')) for val in file.readlines()[0].split("/") if val.rstrip('\n')]
        return data

    async def set_views(self, views: bool = False, full_form: bool = True):
        with open(f"{self.path}/app/views.txt", encoding="utf-8") as file:
            data = [int(val.rstrip('\n')) for val in file.readlines()[0].split("/") if val.rstrip('\n')]
        if views:
            data[0] += 1
        elif full_form:
            data[1] += 1
        with open(f"{self.path}/app/views.txt", encoding="utf-8", mode="w") as file:
            data = f"{data[0]}/{data[1]}"
            file.write(data)

    async def get_text_img(self) -> [str, str | None]:
        """[text, img_path]"""
        with open(f"{self.path}/our_message/message_text.txt", encoding="utf-8") as file:
            text = file.read()
            image_path = None
        if len(os.listdir(f"{self.path}/our_message")) == 2:
            for file in os.listdir(f"{self.path}/our_message"):
                if file != 'message_text.txt':
                    image_path = f"{self.path}/our_message/{file}"
                    break

        return [text, image_path]


config = Config()
