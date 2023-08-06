class BaseHandler:
    # 客户端数量 cur, max
    @classmethod
    def get_client_count(cls, user):
        return 1, 1

    # 客户端超限后的数据  [{'token', 'app', 'os', 'ip', 'region', 'created_time_ago'}]
    @classmethod
    def get_exceed_clients_data_on_auth_success(cls, user):
        return []

    # 已有的device_id是否有效
    @classmethod
    def validate_device_id(cls, user, device_id):
        return False

    # 身份验证成功后, 处理保存device_id等, 并返回token
    @classmethod
    def on_auth_succeed_get_token(cls, request, auth_ctx, user):
        pass

    # 踢人时, 处理清理session等
    @classmethod
    def on_kick_session(cls, user, token_to_expire):
        pass
