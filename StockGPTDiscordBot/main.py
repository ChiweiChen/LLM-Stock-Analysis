import discord
from discord import app_commands
from discord.ext import commands
import my_commands.database
from my_commands.stock_price import stock_price
from my_commands.stock_news import stock_news
from my_commands.stock_value import stock_fundamental
from my_commands.stock_gpt import stock_gpt
from my_commands.dict_tabulate import dict_to_tabulate
import os

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} 已登入')
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)}")
    except Exception as e:
        print(e)

# Stock price data


@client.tree.command(name="stock_price",
                     description="搜尋最近股價資料")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_stock(interaction: discord.Interaction, stock_id: str):
    data = stock_price(stock_id)
    stock_data = dict_to_tabulate(data)
    stock_block = "```\n" + stock_data + "```"
    title = f'{stock_id} 各日成交資訊'

    embed = discord.Embed(title=title, description=stock_block)
    await interaction.response.send_message(embed=embed)

# Fundamentals Data


@client.tree.command(name="stock_value",
                     description="搜尋季營收報表資料")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_value(interaction: discord.Interaction, stock_id: str):
    data = stock_fundamental(stock_id)
    stock_data = dict_to_tabulate(data)
    stock_block = "```\n" + stock_data + "```"
    title = f'{stock_id} 個股季營收報表資料'

    embed = discord.Embed(title=title, description=stock_block)
    await interaction.response.send_message(embed=embed)

# News Data


@client.tree.command(name="stock_news",
                     description="搜尋新聞")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_news(interaction: discord.Interaction, stock_id: str):
    data = stock_news(stock_id, add_content=False)
    stock_data = dict_to_tabulate(data)
    stock_block = "```\n" + stock_data + "```"
    title = f'{stock_id} 新聞資料'

    embed = discord.Embed(title=title, description=stock_block)
    await interaction.response.send_message(embed=embed)

# StockGPT


@client.tree.command(name="stock_gpt", description="讓 AI 來分析")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_ai(interaction: discord.Interaction, stock_id: str):

    await interaction.response.defer()

    gpt_reply = stock_gpt(stock_id)
    await interaction.followup.send(gpt_reply)

client.run(token)
