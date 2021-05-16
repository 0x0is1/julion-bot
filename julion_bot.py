from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
import libjulion, requests, os, discord, json
from discord.ext import commands, tasks
from bs4 import BeautifulSoup as scraper
from more_itertools import sliced

bot_name='Julion - The Poet'

info = {}
REFRESH_TIME=300

def embed_generator(data, t):
    separator=['. ', '\r'][t]
    title, poetry, poet = data
    subembeds = []
    try:
        sliced_data=list(sliced(poetry, 980))
        embed = discord.Embed(title=title, color=0x71368a)
        embed.add_field(name=poet, value=sliced_data[0], inline=False)
        sliced_data.pop(0)
        left_over='-'
        for i in sliced_data:
            sembed=discord.Embed(title='continued...', color=0x71368a)
            s=i.split(separator)[-1]
            i=i.replace(s, '')
            sembed.add_field(name='-', value=left_over+i, inline=False)
            subembeds.append(sembed)
            left_over='-'
            left_over+=s
        return embed, subembeds
    except IndexError:pass

def enisable_text_channel(channel_id, status, lang_code):
    global info
    info[str(channel_id)][lang_code]=status
    with open('info.json', 'w') as filename:
        json.dump(info, filename)

def help_embed():
    embed = discord.Embed(title=format(bot_name), color=0x71368a)
    embed.add_field(
        name="Description:", value="This bot is designed for posting Hindi and English poems automatically on discord.", inline=False)
    embed.add_field(
        name="**Commands:**\n", value="`register` : Command used for registering this channel.\n`deregister` : Command used for deregistering this channel.\n`enable [hindi/english]` : Command used for enabling language of poem in this channel. \n `disable [hindi/english]` : Command used for disabling language of poem in this channel.", inline=False)
    embed.add_field(
        name="Invite: ", value="You can get invite link by typing `invite`")
    embed.add_field(
        name="Source: ", value="You can get source code by typing `source`")
    embed.add_field(
        name="Credits: ", value="You can get credits info by typing `credits`")
    return embed

def invite_embed():
    embed = discord.Embed(title='{} Invite'.format(bot_name),url='https://discord.com/api/oauth2/authorize?client_id=843522585596788747&permissions=51264&scope=bot',
                description='Invite {} on your server.'.format(bot_name), color=0x71368a)
    return embed

def source_embed():
    source_code = 'https://github.com/0x0is1/APOD-bot'
    embed = discord.Embed(title='{} Source code'.format(bot_name),
                          url=source_code,
                          description='Get {} Source Code.'.format(bot_name), color=0x71368a)
    return embed

bot = commands.Bot(command_prefix='%')
bot.remove_command('help')

@bot.command(name='help')
async def help(ctx):
    embed = help_embed()
    await ctx.send(embed=embed)

@tasks.loop(seconds=REFRESH_TIME)
async def main_fun():
    global info
    en_url=requests.get(url=libjulion.random_url_generator(0))
    en_soup=scraper(en_url.content, 'html.parser')
    en_data=libjulion.english_poetry_generator(en_soup)
    hi_url=requests.get(url=libjulion.random_url_generator(1))
    hi_soup=scraper(hi_url.content, 'html.parser')
    hi_data=libjulion.hindi_poetry_generator(hi_soup)
    channel_ids = list(info.keys())
    for channel_id in channel_ids:
        en_status=info[channel_id][0]
        hi_status=info[channel_id][1]
        if en_status=='ON':
            embed=embed_generator(en_data, 0)
            channel_ob = bot.get_channel(int(channel_id))
            try:
                await channel_ob.send(embed=embed[0])
                for i in embed[1]:await channel_ob.send(embed=i)
            except TypeError:pass
        if hi_status=='ON':
            embed=embed_generator(hi_data, 1)
            channel_ob = bot.get_channel(int(channel_id))
            try:
                await channel_ob.send(embed=embed[0])
                for i in embed[1]:await channel_ob.send(embed=i)
            except TypeError:pass

@bot.event
async def on_ready():
    global info
    info = json.load(open('info.json', 'r'))
    print('Bot status: Online.')
    main_fun.start()

@bot.command()
async def source(ctx):
    embed = source_embed()
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! `{}ms`'.format(round(bot.latency * 1000)))

@bot.command()
async def credits(ctx):
    embed = discord.Embed(title=format(bot_name), color=0x71368a)
    embed.add_field(name='Disclaimer', value='This API is Owned by `Kavyashala` and `poetry.com`.\nWe do not claim any site related property.\nWe do not promote any illegal use of this API/Bot.', inline=False)
    embed.add_field(name='Developer', value='0x0is1', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def status(ctx):
    global info
    channel_id = ctx.message.channel.id
    channels = info
    channel_ids = list(channels.keys())
    if str(channel_id) in channel_ids:
        embed = discord.Embed(color=0x71368a)
        s=channels[str(channel_id)]
        embed.add_field(name='Status:', value='English: {0}\nHindi: {1}'.format(s[0], s[1]), inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def enable(ctx, lang='english'):
    lang_code={'english': 0, 'hindi': 1}[lang]
    channel_id = ctx.message.channel.id
    enisable_text_channel(channel_id, 'ON', lang_code)
    await ctx.message.add_reaction('✅')

@bot.command()
async def disable(ctx, lang='english'):
    lang_code={'english': 0, 'hindi': 1}[lang]
    channel_id = ctx.message.channel.id
    enisable_text_channel(channel_id, 'OFF', lang_code)
    await ctx.message.add_reaction('✅')

@bot.command()
async def deregister(ctx):
    channel_id = ctx.message.channel.id
    channels = json.load(open('info.json', 'r'))
    channel_ids = list(channels.keys())
    if str(channel_id) in channel_ids:
        global info
        info.pop(str(channel_id))
        with open('info.json', 'w') as filename:
            json.dump(info, filename)
        embed = discord.Embed(color=0x71368a)
        embed.add_field(name='Info: ',
                        value='This channel is no more subscribed for R.O.C.E \n Use `enable` or `disable` commands to resubscribe.', inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def register(ctx):
    channel_id = ctx.message.channel.id
    channels = json.load(open('info.json', 'r'))
    channel_ids = list(channels.keys())
    if not str(channel_id) in channel_ids:
        global info
        info[str(channel_id)] = []
        info[str(channel_id)].append('OFF')
        info[str(channel_id)].append('OFF')
        with open('info.json', 'w') as filename:
            json.dump(info, filename)
        embed = discord.Embed(color=0x71368a)
        embed.add_field(name='Info: ', value='This channel is no more subscribed now. \n Use `enable` or `disable` commands to unsubscribe.', inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(message='This channel is already registered.')

@disable.error
async def disable_error(ctx, error):
    await ctx.send('`Channel is not registered. Please use register command to register.`')
    print(error)

@enable.error
async def enable_error(ctx, error):
    await ctx.send('`Channel is not registered. Please use register command to register.`')
    print(error)

@register.error
async def register_error(ctx, error):
    await ctx.send('`Channel might be already registered.`')
    print(error)

@deregister.error
async def deregister_error(ctx, error):
    await ctx.send('`Channel might not be already registered.`')
    print(error)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('`Unknown command` \n Please use right command to operate. `help` for commands details.')
    if isinstance(error, CommandInvokeError):
        return
    print(error)

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
