import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# Board Model (catalog)
class BoardModelChannelResponse(BaseModel):
    id: uuid.UUID
    channel_number: int
    direction: str
    default_gpio_pin: int
    supports_pullup: bool
    supports_pulldown: bool
    supports_pwm: bool
    label: str | None

    model_config = {"from_attributes": True}


class BoardModelResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    platform: str
    board_variant: str
    image_url: str | None
    is_active: bool
    specifications: dict | None
    channels: list[BoardModelChannelResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class BoardModelChannelCreate(BaseModel):
    channel_number: int
    direction: str = Field(..., pattern=r"^(input|output)$")
    default_gpio_pin: int
    supports_pullup: bool = True
    supports_pulldown: bool = True
    supports_pwm: bool = False
    label: str | None = None


class BoardModelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    platform: str = "ESP32"
    board_variant: str = Field(..., min_length=1, max_length=100)
    image_url: str | None = None
    channels: list[BoardModelChannelCreate] = []


# Board Instance
class ChannelConfig(BaseModel):
    channel_number: int
    name: str = ""
    gpio_pin: int | None = None
    pull_mode: str = "none"
    inverted: bool = False
    debounce_ms: int = 0
    is_enabled: bool = True


class BoardInstanceCreate(BaseModel):
    board_model_id: uuid.UUID
    name: str = Field(..., min_length=1, max_length=255)
    esphome_name: str = Field(..., min_length=1, max_length=100, pattern=r"^[a-z0-9_]+$")
    device_address: str | None = None


class BoardInstanceChannelResponse(BaseModel):
    id: uuid.UUID
    channel_number: int
    direction: str
    name: str
    gpio_pin: int
    pull_mode: str
    inverted: bool
    debounce_ms: int
    is_enabled: bool

    model_config = {"from_attributes": True}


class BoardInstanceResponse(BaseModel):
    id: uuid.UUID
    name: str
    esphome_name: str
    device_address: str | None
    board_model_id: uuid.UUID
    channels: list[BoardInstanceChannelResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}
