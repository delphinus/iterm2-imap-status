#!/usr/bin/env python3
from datetime import datetime
from iterm2 import (
    Connection,
    PositiveFloatingPointKnob,
    StatusBarComponent,
    StatusBarRPC,
    StringKnob,
    run_forever,
)
from iterm2.statusbar import Knob
from subprocess import CalledProcessError, check_output
from typing import Any, Dict
from imaplib import IMAP4_SSL


class Config:
    def __init__(self, server: str, port: int, username: str):
        self.__id = ":".join([server, str(port), username])
        self.server = server
        self.port = port
        self.username = username

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Config):
            return self.__id == other.__id
        return False

    def __hash__(self) -> int:
        return hash(self.__id)

    def __str__(self) -> str:
        return f"{self.username} on {self.server}:{self.port}"


class Cache:
    __cache: Dict[Config, Dict[str, int]] = {}

    def __init__(self, expires: int = 29) -> None:
        self.expires = expires

    def is_old(self, cfg: Config, now: int) -> bool:
        if cfg in self.__cache:
            return now > self.__cache[cfg]["calculated"] + self.expires
        return True

    def get(self, cfg: Config) -> int:
        return self.__cache[cfg]["count"] if cfg in self.__cache else 0

    def set(self, cfg: Config, count: int, now: int) -> None:
        self.__cache[cfg] = {"count": count, "calculated": now}


class Fetcher:
    cache = Cache()

    def run(self, cfg: Config) -> int:
        now = int(datetime.now().timestamp())
        if self.cache.is_old(cfg, now):
            count = self._calculate(cfg)
            self.cache.set(cfg, count, now)
        else:
            print("cache hit!!")
        return self.cache.get(cfg)

    def _calculate(self, cfg: Config) -> int:
        print(f"fetching...: {cfg}")
        imap = IMAP4_SSL(cfg.server, cfg.port)
        (result, [data]) = imap.login(cfg.username, self.password(cfg))
        if result != "OK":
            raise RuntimeError("error occurred on login")
        (result, [data]) = imap.select("INBOX")
        return int(data.decode("utf-8"))

    def password(self, cfg: Config) -> str:
        try:
            out: bytes = check_output(
                args=[
                    "security",
                    "find-internet-password",
                    "-a",
                    cfg.username,
                    "-s",
                    cfg.server,
                    "-P",
                    str(cfg.port),
                    "-w",
                ]
            )
            return out.decode("utf-8").strip()
        except CalledProcessError:
            print("cannot access to keychain")
            raise


async def main(connection: Connection) -> None:
    component: StatusBarComponent = StatusBarComponent(
        "IMAP Status",
        "Show count of new messages",
        [
            StringKnob("Server", "imap.example.com", "", "server"),
            PositiveFloatingPointKnob("Port", 993, "port"),
            StringKnob("Username", "foo@example.com", "", "username"),
            StringKnob("Prefix", "", "📩", "prefix"),
        ],
        "📩 20",
        30,
        "dev.delphinus.imap_status",
    )
    fetcher = Fetcher()

    @StatusBarRPC
    async def imap_status(knobs: Dict[str, Any]) -> str:
        cfg = Config(knobs["server"], knobs["port"], knobs["username"])
        count = fetcher.run(cfg)
        return f"{knobs['prefix']} {count}"

    await component.async_register(connection, imap_status, timeout=None)


if __name__ == "__main__":
    run_forever(main)
