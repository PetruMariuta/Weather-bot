import discord
color = 0xFF001A
key_features = {
    'temp' : 'Temperatura °C 🌡',
    'feels_like' : 'Se simte ca 🌡',
    'temp_min' : 'Temperatura Minima 🌡',
    'temp_max' : ' Temperatura Maxima 🌡'
}

def parse_data(data):
    data = data["main"]
    
    del data["humidity"]
    del data["pressure"]
    return data



def weather_message(data,location): #embedded message
  location = location.title()
  message=discord.Embed(title=f" Vremea in {location}",description=f"Vremea astazi in {location}:",color=color)
  
  for key in data:
        message.add_field(
           
            name=key_features[key],                      
            value=f"{int(data[key])} °C",
            inline=False  #  vertical message
        )
  return message