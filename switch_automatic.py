#!/usr/bin/env python3

import asyncio
import iterm2

async def change_profiles(connection, preset):
    # Update the list of all profiles and iterate over them.
    profiles=await iterm2.PartialProfile.async_query(connection)
    for partial in profiles:
        # Fetch the full profile and then set the color preset in it.
        profile = await partial.async_get_full_profile()
        await profile.async_set_color_preset(preset)

async def select_preset(connection, theme):
    if "dark" in theme:
        preset = await iterm2.ColorPreset.async_get(connection, "my_dark")
    else:
        preset = await iterm2.ColorPreset.async_get(connection, "my_light")
    return preset

async def main(connection):
    print("Main started")
    app = await iterm2.async_get_app(connection)
    theme = await app.async_get_theme()
    print(theme)
    preset = await select_preset(connection, theme)
    print("Before changing profiles")
    await change_profiles(connection, preset)
    print("After changing profiles")

    async with iterm2.VariableMonitor(connection, iterm2.VariableScopes.APP, "effectiveTheme", None) as mon:
        print("Before loop")
        while True:
            print("In loop")
            # Block until theme changes
            theme = await mon.async_get()
            print("Theme changed")
            # Themes have space-delimited attributes, one of which will be light or dark.
            parts = theme.split(" ")
            preset = await select_preset(connection, theme)
            await change_profiles(connection, preset)


iterm2.run_forever(main)
