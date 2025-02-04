from dataclasses import dataclass, field


@dataclass
class BlacklistTokensInMemory:
    blacklist: list[str] = field(default_factory=list)

    def add_token(self, token: str) -> None:
        self.blacklist.append(token)

    def remove_token(self, token: str) -> None:
        self.blacklist.remove(token)

    def contains_token(self, token: str) -> bool:
        return token in self.blacklist
