import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')

@bot.command()
async def criar_temp(ctx, *, nome_canal="Canal Temporário"):
    # Verifica se o autor do comando está em um canal de voz
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        return

    # Cria o canal temporário
    categoria = ctx.author.voice.channel.category
    canal_temp = await categoria.create_voice_channel(nome_canal)
    
    # Move o autor para o novo canal
    await ctx.author.move_to(canal_temp)
    
    await ctx.send(f"Canal temporário '{nome_canal}' criado!")

@bot.event
async def on_voice_state_update(member, before, after):
    # Verifica se o membro saiu de um canal
    if before.channel is not None and after.channel != before.channel:
        # Verifica se o canal está vazio
        if len(before.channel.members) == 0:
            # Verifica se o nome do canal começa com "Canal Temporário"
            if before.channel.name.startswith("Canal Temporário"):
                await before.channel.delete()

# Substitua 'TOKEN_DO_SEU_BOT' pelo token real do seu bot
bot.run('TOKEN_DO_SEU_BOT')
