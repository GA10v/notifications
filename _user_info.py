from utils.get_user_info import FakeUserInfo, UserInfo

if __name__ == '__main__':
    # получить реальные данные из Auth:
    client = UserInfo()
    info = client.get_user_info(user_id='dede8f0b-9e47-45f1-b00c-a216d6bbf42b')
    print(info)  # noqa: T201
    # получить фейковые данные данные:
    fake_client = FakeUserInfo()
    fake_info = fake_client.get_user_info()
    print(fake_info)  # noqa: T201
