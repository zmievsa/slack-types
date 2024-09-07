from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, Field

from enum import Enum


class StrEnum(str, Enum):  # pragma: no cover # It's code from CPython so no need to cover it
    """
    Enum where members are also (and must be) strings
    """

    def __new__(cls, *values: str):
        "values must already be of type `str`"
        if len(values) > 3:
            raise TypeError(f"too many arguments for str(): {values!r}")
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError(f"{values[0]!r} is not a string")
        elif len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError(f"encoding must be a string, not {values[1]!r}")
        elif len(values) == 3:  # noqa: SIM102
            # check that errors argument is a string
            if not isinstance(values[2], str):
                raise TypeError(f"errors must be a string, not {values[2]!r}")
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    @staticmethod
    def _generate_next_value_(name: str, start, count, last_values) -> str:  # noqa: ANN001, ARG004
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()

    def __str__(self) -> str:
        return str.__str__(self)

    def __format__(self, __format_spec: str) -> str:  # pyright: ignore [reportIncompatibleMethodOverride]
        return str.__format__(self, __format_spec)


class SlackInteractionPayloadType(StrEnum):
    block_actions = "block_actions"
    interactive_message = "interactive_message"
    view_submission = "view_submission"
    shortcut = "shortcut"
    message_action = "message_action"


class SlackViewType(StrEnum):
    modal = "modal"


class Team(BaseModel):
    id: str
    domain: str


class User(BaseModel):
    id: str
    username: str
    team_id: str | None


class Container(BaseModel):
    type: str
    message_ts: str
    attachment_id: int
    channel_id: str
    is_ephemeral: bool
    is_app_unfurl: bool


class Channel(BaseModel):
    id: str
    name: str


class Message(BaseModel):
    bot_id: Optional[str]
    type: str
    text: str
    user: str
    ts: str


class Text(BaseModel):
    type: Literal["plain_text", "mrkdwn"]
    text: str
    emoji: Optional[bool] = None
    verbatim: Optional[bool] = None


class Action(BaseModel):
    action_id: str | None
    block_id: str
    text: Text
    value: str
    type: str
    action_ts: str


class Element(BaseModel):
    type: str
    action_id: str | None
    text: Text | str | None
    elements: "Optional[List[Element]]"


class Block(BaseModel):
    block_id: str | None
    type: str
    text: Optional[Text]
    elements: Optional[List[Element]]
    element: Optional[Element]
    label: Optional[Text]


class ViewStateValues(BaseModel):
    values: dict


class ViewResponseURL(BaseModel):
    block_id: str
    action_id: str
    channel_id: str
    response_url: str


class View(BaseModel):
    type: Literal[SlackViewType.modal]
    blocks: List[Block]
    title: Text | str | None
    close: Text
    submit: Text
    id: str | None
    team_id: str | None
    private_metadata: str | None
    callback_id: str | None
    state: ViewStateValues | None
    hash: str | None
    clear_on_close: bool | None
    notify_on_close: bool | None
    previous_view_id: Optional[str]
    root_view_id: str | None
    app_id: str | None
    external_id: str | None
    app_installed_team_id: str | None
    bot_id: str | None
    response_urls: list[ViewResponseURL] | None


class MessageActionUser(BaseModel):
    id: str
    name: str


class MessageActionMessage(BaseModel):
    type: str
    user: str
    ts: str
    text: str


class SlackInteractiveMessageWebhookPayload(BaseModel):
    type: Literal[SlackInteractionPayloadType.interactive_message]
    trigger_id: str
    token: str
    team: Team
    user: User
    api_app_id: str
    container: Container
    channel: Channel
    message: Message
    response_url: str
    actions: List[Action]


class SlackBlockActionsWebhookPayload(BaseModel):
    type: Literal[SlackInteractionPayloadType.block_actions]
    team: Team
    user: User
    api_app_id: str
    token: str
    container: Container
    trigger_id: str
    view: View
    actions: List[Action]


class SlackGlobalShortcutWebhookPayload(BaseModel):
    type: Literal[SlackInteractionPayloadType.shortcut]
    token: str
    action_ts: str
    team: Team
    user: User
    callback_id: str
    trigger_id: str


class MessageActionPayload(BaseModel):
    type: Literal[SlackInteractionPayloadType.message_action]
    token: str
    callback_id: str
    trigger_id: str
    response_url: str
    team: Team
    channel: Channel
    user: MessageActionUser
    message: MessageActionMessage


class ViewSubmissionPayload(BaseModel):
    type: Literal[SlackInteractionPayloadType.view_submission]
    team: Team
    user: User
    view: View


class SlackWebhookPayload(BaseModel):
    __root__: Annotated[
        ViewSubmissionPayload
        | SlackBlockActionsWebhookPayload
        | SlackGlobalShortcutWebhookPayload
        | SlackInteractiveMessageWebhookPayload
        | MessageActionPayload,
        Field(discriminator="type"),
    ]
