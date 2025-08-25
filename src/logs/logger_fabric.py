class LoggerFabric:
    Role = Literal["buyer", "seller", "admin"]

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def get_service(self, role: Role) -> IAuthService:
        if role == "buyer":
            return BuyerService(self.uow)
        elif role == "seller":
            return SellerService(self.uow)
        elif role == "admin":
            return AdminService(self.uow)
        raise ValueError(f"Unknown role: {role}")