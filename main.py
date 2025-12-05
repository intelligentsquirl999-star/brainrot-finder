-- INJECT THIS ON EACH ALT (Solara/Wave) – REAL PET SNIPER
local TARGET_PETS = {
    "Noobini Pizzanini","La Vacca Saturno Saturno Saturnita","Bisonte Giuppitere",
    "Karkerkar Kurkur","Los Matteos","Los Tralaleritos","Las Tralaleritas",
    "Graipuss Medussi","La Grande Combinasion","Torrtuginni Dragonfruitini",
    "Pot Hotspot","Las Vaquitas Saturnitas","Chicleteira Bicicleteira",
    "Agarrini la Palini","Dragon Cannelloni","Los Combinasionas",
    "Los Hotspotsitos","Esok Sekolah","Nuclearo Dinossauro",
    "Sammyni Spyderini","Blackhole Goat","Dul Dul Dul"
}

local PLACE_ID = 109983668079237

spawn(function()
    while wait(3) do
        local servers = game.HttpService:JSONDecode(game:HttpGet(
            "https://games.roblox.com/v1/games/"..PLACE_ID.."/servers/Public?sortOrder=Asc&limit=100"
        )).data

        for _, srv in pairs(servers) do
            if srv.playing < srv.maxPlayers then
                game:GetService("TeleportService"):TeleportToPlaceInstance(PLACE_ID, srv.id)
                wait(8) -- wait for load

                -- NOW WE CAN SEE PET NAMES
                for _, player in pairs(game.Players:GetPlayers()) do
                    if player ~= game.Players.LocalPlayer then
                        for _, pet in pairs(player:FindFirstChild("PlayerGui") and player.PlayerGui:GetDescendants() or {}) do
                            if pet:IsA("TextLabel") and table.find(TARGET_PETS, pet.Text) then
                                game.StarterGui:SetCore("SendNotification",{
                                    Title = "FOUND!";
                                    Text = pet.Text.." in server!";
                                    Duration = 10
                                })
                                wait(300) -- stay 5 min
                            end
                        end
                    end
                end
                -- Leave and continue
                game:GetService("TeleportService"):Teleport(PLACE_ID)
            end
        end
    end
end)
