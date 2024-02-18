from __future__ import annotations
from .const import DOMAIN
from .isapi import ISAPI
from homeassistant.config_entries import ConfigEntry, ConfigFlow
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult
from http import HTTPStatus
from httpx import ConnectTimeout, HTTPStatusError
from typing import Any
import asyncio
import logging
import voluptuous as vol


_LOGGER = logging.getLogger(__name__)


class HikvisionFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for hikvision device."""

    VERSION = 1
    _reauth_entry: ConfigEntry | None = None

    async def get_schema(self, user_input: dict[str, Any]):
        """Get schema with default values or entered by user"""
        return vol.Schema(
            {
                vol.Required(CONF_HOST, default=user_input.get(CONF_HOST, "http://")): str,
                vol.Required(CONF_USERNAME, default=user_input.get(CONF_USERNAME, "")): str,
                vol.Required(CONF_PASSWORD, default=user_input.get(CONF_PASSWORD, "")): str,
            }
        )

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle a flow initiated by the user."""

        errors = {}

        if user_input is not None:
            try:
                host = user_input[CONF_HOST]
                username = user_input[CONF_USERNAME]
                password = user_input[CONF_PASSWORD]

                isapi = ISAPI(host, username, password)
                await isapi.get_device_info()

                if self._reauth_entry:
                    self.hass.config_entries.async_update_entry(self._reauth_entry, data=user_input)
                    self.hass.async_create_task(self.hass.config_entries.async_reload(self._reauth_entry.entry_id))
                    return self.async_abort(reason="reauth_successful")

                await self.async_set_unique_id({(DOMAIN, isapi.device_info.serial_no)})
                self._abort_if_unique_id_configured()

            except HTTPStatusError as error:
                status_code = error.response.status_code
                if status_code == HTTPStatus.UNAUTHORIZED:
                    errors["base"] = "invalid_auth"
                elif status_code == HTTPStatus.FORBIDDEN:
                    errors["base"] = "insufficient_permission"
                _LOGGER.error("ISAPI error %s", error)
            except ConnectTimeout:
                errors["base"] = "cannot_connect"
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error("Unexpected exception %s", ex)
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=isapi.device_info.name, data=user_input)

        schema = await self.get_schema(user_input or {})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> FlowResult:
        """Schedule reauth."""
        _LOGGER.warning("Attempt to reauth in 120s")
        self._reauth_entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        await asyncio.sleep(120)
        return await self.async_step_user(entry_data)
