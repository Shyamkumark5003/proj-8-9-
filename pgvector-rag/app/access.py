from dataclasses import dataclass

VALID_ROLES = {"viewer", "manager", "admin"}


@dataclass(frozen=True)
class UserContext:
    tenant_id: str
    roles: tuple


# Real project la idhu login/JWT la irundhu varum.
# Server side la irukkanum, user input la irundhu edukka koodaadhu.
USERS = {
    "viewer_acme":  UserContext("acme", ("viewer",)),
    "manager_acme": UserContext("acme", ("manager",)),
    "admin_acme":   UserContext("acme", ("admin",)),
    "viewer_beta":  UserContext("beta", ("viewer",)),
}


def get_user(username: str) -> UserContext:
    user = USERS.get(username)
    if user is None:
        raise PermissionError(f"Unknown user: {username}")
    if not set(user.roles) <= VALID_ROLES:
        raise PermissionError("Invalid role")
    return user