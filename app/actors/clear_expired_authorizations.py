from ..repositories.user import UserRepository


def clear_expired_authorizations(user_repository=UserRepository()):
    expired_users = user_repository.find_expired_authorizations()

    if expired_users:
        user_repository.delete_many(expired_users)
