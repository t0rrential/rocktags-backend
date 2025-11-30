from __future__ import annotations
from os.path import exists, getsize
from os import remove

from findmy import (
    AppleAccount,
    AsyncAppleAccount,
    LocalAnisetteProvider,
    LoginState,
    RemoteAnisetteProvider,
    SmsSecondFactorMethod,
    TrustedDeviceSecondFactorMethod,
)


def _login_sync(account: AppleAccount) -> None:
    email = input("email?  > ")
    password = input("passwd? > ")

    state = account.login(email, password)

    if state == LoginState.REQUIRE_2FA:  # Account requires 2FA
        # This only supports SMS methods for now
        methods = account.get_2fa_methods()

        # Print the (masked) phone numbers
        for i, method in enumerate(methods):
            if isinstance(method, TrustedDeviceSecondFactorMethod):
                print(f"{i} - Trusted Device")
            elif isinstance(method, SmsSecondFactorMethod):
                print(f"{i} - SMS ({method.phone_number})")

        ind = int(input("Method? > "))

        method = methods[ind]
        method.request()
        code = input("Code? > ")

        # This automatically finishes the post-2FA login flow
        method.submit(code)


async def _login_async(account: AsyncAppleAccount) -> None:
    email = input("email?  > ")
    password = input("passwd? > ")

    state = await account.login(email, password)

    if state == LoginState.REQUIRE_2FA:  # Account requires 2FA
        # This only supports SMS methods for now
        methods = await account.get_2fa_methods()

        # Print the (masked) phone numbers
        for i, method in enumerate(methods):
            if isinstance(method, TrustedDeviceSecondFactorMethod):
                print(f"{i} - Trusted Device")
            elif isinstance(method, SmsSecondFactorMethod):
                print(f"{i} - SMS ({method.phone_number})")

        ind = int(input("Method? > "))

        method = methods[ind]
        await method.request()
        code = input("Code? > ")

        # This automatically finishes the post-2FA login flow
        await method.submit(code)


def get_account_sync(
    store_path: str,
    anisette_url: str | None,
    libs_path: str | None,
) -> AppleAccount:
    """Tries to restore a saved Apple account, or prompts the user for login otherwise. (sync)"""
    if libs_path and exists(libs_path) and getsize(libs_path) <= 0:
        remove(libs_path)

    try:
        binarySize = getsize(libs_path) if libs_path else -1
        print(f"Size of binary is {binarySize}.")
        if (binarySize == 0):
            remove(store_path)
        acc = AppleAccount.from_json(store_path, anisette_libs_path=libs_path)
    except FileNotFoundError:
        ani = (
            LocalAnisetteProvider(libs_path=libs_path)
            if anisette_url is None
            else RemoteAnisetteProvider(anisette_url)
        )
        acc = AppleAccount(ani)
        _login_sync(acc)

        acc.to_json(store_path)

    return acc


async def get_account_async(
    store_path: str,
    anisette_url: str | None,
    libs_path: str | None,
) -> AsyncAppleAccount:
    """Tries to restore a saved Apple account, or prompts the user for login otherwise. (async)"""
    if libs_path and exists(libs_path) and getsize(libs_path) <= 0:
        remove(libs_path)

    try:
        acc = AsyncAppleAccount.from_json(store_path, anisette_libs_path=libs_path)
    except FileNotFoundError or (exists(store_path) and getsize(store_path) <= 0):
        if exists(store_path) and getsize(store_path) <= 0:
            remove(store_path)
        
        ani = (
            LocalAnisetteProvider(libs_path=libs_path)
            if anisette_url is None
            else RemoteAnisetteProvider(anisette_url)
        )
        acc = AsyncAppleAccount(ani)
        await _login_async(acc)

        acc.to_json(store_path)

    return acc