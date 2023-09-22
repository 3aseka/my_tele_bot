from dataclasses import dataclass

@dataclass
class Config:
    #токен бота
    token: str = ''
    #токен админа
    admin_ids: int = ''
    #токен платежной системы
    pay_token: str = ''
    token_p2p: str = 'P2P_TOKEN'